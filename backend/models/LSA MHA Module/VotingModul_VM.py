import time
import random
import logging

class VotingModule:
    def __init__(self, game_state, prompt_builder, gpt_client, consensus_checker, moderator, global_history, reflection, logger=None):
        self.game_state = game_state
        self.prompt_builder = prompt_builder
        self.gpt_client = gpt_client  # GPT interaction instance
        self.consensus_checker = consensus_checker
        self.moderator = moderator
        self.global_history = global_history
        self.reflection = reflection
        self.logger = logger or logging.getLogger(__name__)  # Use provided logger or create a new one

    def night_phase(self, round_number: int) -> str:
        print(f"Night phase started for Round {round_number}.")
        self.moderator.handle_phase_transition("night", round_number)

        # Activate werewolves
        werewolves = self.game_state.get_players_with_role("werewolf")
        if not werewolves:
            print("No werewolves found. Skipping night phase.")
            return "No Elimination"

        for werewolf in werewolves:
            self.game_state.activate_player(werewolf)

        eliminated_player = None
        while not eliminated_player:
            for werewolf in werewolves:
                valid_targets = self.game_state.get_valid_targets(werewolf)
                print(f"Valid targets for {werewolf}: {valid_targets}")
                prompt = self.prompt_builder.build_night_prompt(
                    player=werewolf,
                    role=self.game_state.get_role(werewolf),
                    round_number=round_number,
                    conversation_log=self.game_state.get_conversation_log(werewolf),  # Pass player_id
                    last_statement=self.game_state.players[werewolf]['last_statement'],
                    valid_targets=valid_targets,
                )
                suggestion = self.gpt_client.get_suggestion(prompt, valid_targets)
                print(f"Suggestion for {werewolf}: {suggestion}")
                self.game_state.add_to_conversation_log(werewolf, suggestion)

            # Display the current game state after suggestions
            self.game_state.display_game_state()

            # Call ConsensusChecker to determine elimination
            print("\n--- Checking Consensus ---")
            eliminated_player = self.consensus_checker.check_consensus(
                self.game_state,
                current_player=werewolves[0]  # Or handle for multiple werewolves logically
            )
            if not eliminated_player:
                print("No consensus reached. Retrying.")

        # Finalize elimination and update the game state
        self.game_state.finalize_elimination(eliminated_player)
        print(f"Player {eliminated_player} has been eliminated during the night phase.")
        return eliminated_player

    def day_phase(self, eliminated_player: str, round_number: int) -> str:
        """
        Handles the day phase, including discussions and voting.

        Args:
            eliminated_player (str): The player eliminated during the night phase or "No Elimination".
            round_number (int): The current round number.

        Returns:
            str: The ID of the player eliminated during the day phase or "No Elimination".
        """
        try:
            # Announce eliminated player or lack thereof
            if eliminated_player != "No Elimination":
                print(f"Day phase started for Round {round_number}. Eliminated player: {eliminated_player}")
                self.moderator.announce_elimination(
                    eliminated_player, self.game_state.get_role(eliminated_player)
                )
            else:
                print(f"Day phase started for Round {round_number}. No player was eliminated during the night.")
                self.moderator.announce_elimination(None, None)

            # Activate all players for discussion
            for player in self.game_state.get_remaining_players():
                self.game_state.activate_player(player)
                if player == "Human":
                    self.game_state.deactivate_player(player)

            # Discussion phase
            discussion_ongoing = True
            while discussion_ongoing:
                start_time = time.time()
                while time.time() - start_time < 180:  # 3-minute timer
                    human_input = input("Human Player: ").strip()
                    if human_input:
                        self.game_state.add_to_conversation_log("Human", human_input)
                        print(f"Human Player contributed: {human_input}")

                    for player in self.game_state.get_remaining_players():
                        if player == "Human":
                            continue
                        # Generate prompt for GPT
                        prompt = self.prompt_builder.build_day_prompt(
                            player=player,
                            round_number=round_number,
                            last_statement=self.game_state.get_last_statement(player),
                            conversation_log=self.game_state.get_conversation_log(player),
                            role_strategy=self.reflection.get_strategy(
                                role=self.game_state.get_role(player),
                                phase="day"
                            ),
                            remaining_players=self.game_state.players[player]['remaining_players']
                        )

                        print(f"Prompt for Player {player}:\n{prompt}")  # Debugging: Print the generated prompt

                        # Get suggestion from GPT
                        suggestion = self.gpt_client.get_suggestion(prompt)
                        print(f"GPT Suggestion for Player {player}: {suggestion}")  # Debugging: Print GPT suggestion
                        self.game_state.add_to_conversation_log(player, suggestion)

                        # Display current game state after every GPT output
                        self.game_state.display_game_state()

                # Moderator intervention after the timer ends
                user_choice = input("Continue discussion or vote? (continue/vote): ").lower()
                if user_choice == "vote":
                    discussion_ongoing = False
                elif user_choice == "continue":
                    print("Discussion phase will continue.")
                else:
                    print("Invalid input. Assuming discussion will continue.")

            # Voting phase
            eliminated_player = self.vote_phase(round_number)
            if not eliminated_player:
                eliminated_player = "No Elimination"
                print("No player was eliminated in the voting phase.")
            else:
                print(f"Player {eliminated_player} eliminated in the voting phase.")

            return eliminated_player

        except Exception as e:
            self.logger.error(f"Error during day_phase: {e}")
            print(f"Error encountered during day_phase: {e}")
            return "No Elimination"

    def vote_phase(self, round_number: int) -> str:
        """
        Facilitates the voting phase and determines the player to be eliminated.

        Args:
            round_number (int): The current round number.

        Returns:
            str: The ID of the eliminated player or "No Elimination".
        """
        print(f"Voting phase started for Round {round_number}.")
        votes = {}
        human_player = "Human"

        for player in self.game_state.get_active_players():
            if player != human_player:
                valid_targets = self.game_state.get_valid_targets(player)
                prompt = self.prompt_builder.build_vote_prompt(
                    player=player,
                    role=self.game_state.get_role(player),
                    round_number=round_number,
                    remaining_players=valid_targets
                )
                vote = self.gpt_client.get_suggestion(prompt, valid_targets)
                votes[player] = vote
                print(f"{player} votes to eliminate: {vote}")

        while True:
            valid_targets = self.game_state.get_valid_targets(human_player)
            print(f"Valid targets: {valid_targets}")
            human_vote = input("Human Player, cast your vote: ").strip()
            if human_vote in valid_targets:
                votes[human_player] = human_vote
                break
            print("Invalid vote. Please choose a valid target.")

        eliminated_player = self.resolve_votes(votes)
        if not eliminated_player:
            eliminated_player = "No Elimination"
        else:
            print(f"Player {eliminated_player} eliminated.")
            self.global_history.record_event("elimination", {"player": eliminated_player, "phase": "day"})

        return eliminated_player

    def fallback_elimination(self) -> str:
        valid_targets = self.game_state.get_valid_targets("Human")
        return random.choice(valid_targets) if valid_targets else "No valid players."

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
            return self.fallback_elimination()

        # Count the votes
        vote_counts = {}
        for vote in votes.values():
            vote_counts[vote] = vote_counts.get(vote, 0) + 1

        # Find the player(s) with the highest vote count
        max_votes = max(vote_counts.values(), default=0)
        candidates = [player for player, count in vote_counts.items() if count == max_votes]

        if len(candidates) == 1:
            return candidates[0]  # Clear majority, return the single candidate

        # Handle ties
        print(f"Tie detected among: {candidates}. Selecting randomly.")
        return random.choice(candidates)

