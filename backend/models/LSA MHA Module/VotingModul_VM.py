import time
import random

class VotingModule:
    def __init__(self, game_state, prompt_builder, gpt_client, consensus_checker, moderator, global_history):
        """
        Initializes the Voting Module.

        Args:
            game_state: GameState module for managing player states.
            prompt_builder: PromptBuilder module for creating context-sensitive prompts.
            gpt_client: GPTInteraction module for generating AI-driven suggestions.
            consensus_checker: ConsensusChecker module for checking consensus among players.
            moderator: Moderator module for announcements and phase management.
            global_history: GlobalHistoryModel for recording game events.
        """
        self.game_state = game_state
        self.prompt_builder = prompt_builder
        self.gpt_client = gpt_client  # GPT interaction instance
        self.consensus_checker = consensus_checker
        self.moderator = moderator
        self.global_history = global_history

    def night_phase(self, round_number: int) -> None:
        """
        Handles the night phase of the game and returns the eliminated player.

        Args:
            round_number (int): The current round number.

        Returns:
            str: The ID of the eliminated player, or a placeholder indicating no elimination.
        """
        print(f"Night phase started for Round {round_number}.")
        self.moderator.handle_phase_transition("night", round_number)

        werewolves = self.game_state.get_players_with_role("werewolf")
        eliminated_player = None
        attempts = 0
        timeout = 10

        if not werewolves:
            print("No werewolves found. Skipping night phase.")
            return None  # Exit early if no werewolves

        while not eliminated_player and attempts < timeout:
            for werewolf in werewolves:  # Ensure this is a valid list
                valid_targets = self.game_state.get_valid_targets(werewolf)
                print(f"Valid targets for {werewolf}: {valid_targets}")  # Debug
                last_statement = self.game_state.get_last_statement(werewolf)
                prompt = self.prompt_builder.build_night_prompt(
                    player=werewolf,
                    role=self.game_state.get_role(werewolf),
                    round_number=round_number,
                    conversation_log=self.game_state.get_conversation_log(),
                    last_statement=last_statement,
                    valid_targets=valid_targets,
                )
                suggestion = self.gpt_client.get_suggestion(prompt, valid_targets)
                print(f"Suggestion for {werewolf}: {suggestion}")  # Debug
                self.game_state.add_to_conversation_log(werewolf, suggestion)

            print("\n--- Current Conversation Log ---")
            print(self.game_state.get_conversation_log())

            # Use consensus checker to determine elimination
            eliminated_player = self.consensus_checker.check_consensus(self.game_state, current_player=werewolves[0])
            if eliminated_player:
                print(f"\n*** Consensus reached on Player {eliminated_player}! ***")
                break

            attempts += 1

        # Validate eliminated_player and apply fallback if necessary
        if eliminated_player is None:
            print("No eliminated player determined. Using fallback.")
            eliminated_player = self.fallback_elimination()

        if eliminated_player:
            self.game_state.finalize_elimination(eliminated_player)
        return eliminated_player

    def day_phase(self, eliminated_player: str, round_number: int):
        """
        Handles the day phase, including discussions and voting.

        Args:
            eliminated_player (str): The player eliminated during the night phase or "No Elimination".
            round_number (int): The current round number.
        """
        if eliminated_player != "No Elimination":
            print(f"Day phase started for Round {round_number}. Eliminated player: {eliminated_player}")
            self.moderator.announce_elimination(eliminated_player, self.game_state.get_role(eliminated_player))
        else:
            print(f"Day phase started for Round {round_number}. No player was eliminated during the night.")
            self.moderator.announce_elimination(None, None)

        discussion_ongoing = True
        while discussion_ongoing:
            start_time = time.time()
            while time.time() - start_time < 180:  # Allow 3 minutes for discussion
                human_input = input("Human Player: ").strip()
                if human_input:
                    self.game_state.add_to_conversation_log("Human", human_input)

                for player in self.game_state.get_remaining_players():
                    prompt = self.prompt_builder.build_day_prompt(
                        player=player,
                        round_number=round_number,
                        last_statement=self.game_state.get_last_statement(player),
                        conversation_log=self.game_state.get_conversation_log(),
                        role_strategy=self.game_state.get_strategy(player),
                        remaining_players=self.game_state.get_remaining_players()
                    )
                    suggestion = self.gpt_client.get_suggestion(prompt)
                    self.game_state.add_to_conversation_log(player, suggestion)
                    print(f"{player}: {suggestion}")

            if input("Continue discussion or vote? (continue/vote): ").lower() == "vote":
                discussion_ongoing = False

        # Transition to the voting phase
        eliminated_player = self.vote_phase(round_number)
        print(f"Player {eliminated_player} eliminated in the voting phase.")

    def vote_phase(self, round_number: int) -> str:
        """
        Facilitates the voting phase and determines the player to be eliminated.

        Args:
            round_number (int): The current round number.

        Returns:
            str: The ID of the eliminated player.
        """
        print(f"Voting phase started for Round {round_number}.")
        votes = {}

        for player in self.game_state.get_remaining_players():
            prompt = self.prompt_builder.build_vote_prompt(
                player=player,
                role=self.game_state.get_role(player),
                round_number=round_number,
                remaining_players=self.game_state.get_valid_targets()
            )
            vote = self.gpt_client.get_suggestion(prompt, self.game_state.get_valid_targets())
            votes[player] = vote
            print(f"{player} votes to eliminate: {vote}")

        human_vote = None
        while human_vote not in self.game_state.get_valid_targets():
            human_vote = input(f"Cast your vote. Valid targets: {', '.join(self.game_state.get_valid_targets())}: ")
        votes["Human Player"] = human_vote

        eliminated_player = self.resolve_votes(votes)
        print(f"Player {eliminated_player} eliminated.")
        self.global_history.record_event("elimination", {"player": eliminated_player, "phase": "day"})
        return eliminated_player

    def resolve_votes(self, votes: dict) -> str:
        """
        Resolves votes and determines the eliminated player.

        Args:
            votes (dict): A dictionary of votes where keys are players and values are vote counts.

        Returns:
            str: The ID of the eliminated player.
        """
        if not votes:
            print("No votes to resolve. Returning a fallback elimination.")
            return self.fallback_elimination()  # Ensure a fallback mechanism is called for empty votes

        # Count the votes
        vote_counts = {}
        for vote in votes.values():
            if vote:
                vote_counts[vote] = vote_counts.get(vote, 0) + 1

        # Identify the highest vote count
        max_votes = max(vote_counts.values(), default=0)
        candidates = [player for player, count in vote_counts.items() if count == max_votes]

        if len(candidates) == 1:
            return candidates[0]

        # Tie-breaker logic
        print(f"Tie detected among: {candidates}. Selecting randomly.")
        return random.choice(candidates)

    def fallback_elimination(self) -> str:
        """
        Determines a fallback elimination target if no consensus is reached.

        Returns:
            str: The ID of the fallback elimination target.
        """
        remaining_players = self.game_state.get_valid_targets()
        return random.choice(remaining_players) if remaining_players else "No valid players."
