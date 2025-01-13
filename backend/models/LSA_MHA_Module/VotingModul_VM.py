import time
import logging

class VotingModule:
    def __init__(self, orchestrator, game_state, prompt_builder, gpt_client, consensus_checker, moderator, global_history, reflection, logger=None):
        self.orchestrator = orchestrator
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

        # Deactivate all players
        for player_id in self.game_state.players.keys():
            self.game_state.deactivate_player(player_id)

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
                    game_state=self.game_state
                )
                suggestion = self.gpt_client.get_suggestion(prompt, valid_targets, self.game_state, current_player=werewolf)
                print(f"Suggestion for {werewolf}: {suggestion}")
                self.game_state.add_to_conversation_log(werewolf, suggestion, phase="night")

            # Display the current game state after suggestions
            self.game_state.display_game_state()

            # Call ConsensusChecker to determine elimination
            print("\n--- Checking Consensus ---")
            eliminated_player = self.consensus_checker.check_consensus(
                game_state=self.game_state,
                current_player=werewolves[0]  # Or handle for multiple werewolves logically
            )
            if not eliminated_player:
                print("No consensus reached. Retrying.")

        # Finalize elimination and update the game state
        self.game_state.finalize_elimination(eliminated_player)
        print(f"Player {eliminated_player} has been eliminated during the night phase.")

        self.orchestrator.check_game_end_conditions()

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
                print(f"Wake up everyone! Day phase started for Round {round_number}. Eliminated player: {eliminated_player}")
            else:
                print(f"Day phase started for Round {round_number}. No player was eliminated during the night.")
                self.moderator.announce_elimination(None, None)

            # Activate all players for discussion, including the human player
            for player in self.game_state.get_remaining_players():
                self.game_state.activate_player(player)
                if player == "Human":
                    self.game_state.players[player]["awake"] = True
                self.game_state.players[player]["remaining_players"] = [
                    p for p in self.game_state.get_remaining_players() if p != player
                ]

            self.game_state.display_game_state()  # This should be here
            announcement = self.moderator.announce_elimination(
                eliminated_player, self.game_state.get_role(eliminated_player)
            )
            print(announcement)

            discussion_ongoing = True
            while discussion_ongoing:
                start_time = time.time()
                while time.time() - start_time < 60:  # 1-minute timer
                    human_input = input("Human Player: ").strip()
                    if human_input:
                        self.game_state.add_to_conversation_log("Human", human_input)
                        print(f"Human Player contributed: {human_input}")

                    for player in self.game_state.get_remaining_players():
                        if player == "Human" or not self.game_state.players[player]["remaining"]:
                            continue
                        valid_targets = self.game_state.get_valid_targets(player)
                        prompt = self.prompt_builder.build_day_prompt(
                            player_id=player,
                            round_number=round_number,
                            game_state=self.game_state
                        )
                        suggestion = self.gpt_client.get_suggestion(prompt, valid_targets, self.game_state, current_player=player)
                        print(f"GPT Suggestion for Player {player}: {suggestion}")
                        self.game_state.add_to_conversation_log(player, suggestion, phase="day")

                while True:
                    user_choice = input("Continue discussion or vote? (continue/vote): ").lower().strip()
                    if user_choice == "vote":
                        discussion_ongoing = False
                        break
                    elif user_choice == "continue":
                        print("Discussion phase will continue.")
                        break
                    else:
                        print("Invalid input. Please enter 'continue' or 'vote'.")

            eliminated_player = self.vote_phase(round_number)

            if eliminated_player:
                eliminated_role = self.game_state.get_role(eliminated_player) or "Unknown role"
                announcement = f"During the day, you guys decided to eliminate Player {eliminated_player} ({eliminated_role})."
                print(announcement)
                self.moderator.announce_elimination(eliminated_player, eliminated_role)

                # Finalize elimination
                self.game_state.finalize_elimination(eliminated_player)
                print(f"Player {eliminated_player} ({eliminated_role}) was eliminated during the day phase.")

                # Display the updated game state
                print("\n--- Game State After Voting ---")
                self.game_state.display_game_state()

                # Check if the game has reached an end condition
                self.orchestrator.check_game_end_conditions()

                ready = input("\nAre you ready to continue to the next round? (yes/no): ").strip().lower()
                if ready != "yes":
                    print("Pausing until you're ready...")
                    input("Press Enter when ready to continue.")
            return eliminated_player

        except Exception as e:
            self.logger.error(f"Error during day_phase: {e}")
            print(f"Error encountered during day_phase: {e}")
            return "No Elimination"

    def vote_phase(self, round_number: int) -> str:
        """
        Facilitates the voting phase and determines the eliminated player.

        Args:
            round_number (int): The current round number.

        Returns:
            str: The ID of the eliminated player or "No Elimination".
        """
        print(f"Voting phase started for Round {round_number}.")
        valid_targets = [target for target in self.game_state.get_remaining_players() if target != "Human"]
        human_targets = valid_targets.copy()

        eliminated_player = None

        # Collect votes from agents
        for player in self.game_state.get_remaining_players():

            if player != "Human":
                valid_targets = self.game_state.get_valid_targets(player)
                prompt = self.prompt_builder.build_agent_vote_prompt(
                    player=player,
                    role=self.game_state.get_role(player),
                    round_number=round_number,
                    remaining_players=valid_targets,
                    game_state = self.game_state
                )
                vote = self.gpt_client.get_suggestion(prompt, valid_targets, self.game_state, current_player=player)
                print(f"GPT Suggestion for {player}: {vote}")
                self.game_state.add_to_conversation_log(player, f"{player} votes for {vote}")

                if vote in valid_targets:
                    self.game_state.add_to_conversation_log(player, f"{player} votes for {vote}")

        # Collect the human player's vote
        print("Human Player, cast your vote!")
        human_vote = input(f"Choose from {', '.join(human_targets)}: ").strip()
        if human_vote in human_targets:
            self.game_state.add_to_conversation_log("Human", f"Human Player votes for {human_vote}")
        else:
            print("Invalid vote. Defaulting to 'No Elimination'.")
            return "No Elimination"

        # Analyze votes and determine the eliminated player
        prompt = self.prompt_builder.build_vote_analysis_prompt(
            conversation_log=self.game_state.global_conversation_log,
            valid_targets=valid_targets + ["Human"],  # Include Human as a valid target
            game_state=self.game_state
        )
        gpt_response = self.gpt_client.get_suggestion(prompt, valid_targets, self.game_state, current_player=player)

        print(f"GPT resolved votes: {gpt_response}")

        if "Consensus reached on Player" in gpt_response:
            eliminated_player = gpt_response.split("Player")[-1].strip()

            # Validate the eliminated player
            if eliminated_player in valid_targets:
                role = self.game_state.get_role(eliminated_player)
                self.game_state.finalize_elimination(eliminated_player)
                print(f"Player {eliminated_player} ({role}) was eliminated during the voting phase.")
                return eliminated_player
            else:
                self.logger.error(f"Invalid eliminated player: {eliminated_player}")
        return eliminated_player