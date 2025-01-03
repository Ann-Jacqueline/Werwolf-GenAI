import logging

class ConsensusChecker:
    """
    Checks for consensus among players using GPT and fallback mechanisms.
    """
    def __init__(self, gpt_interaction, prompt_builder, logger=None, moderator=None):
        self.gpt_interaction = gpt_interaction
        self.prompt_builder = prompt_builder
        self.logger = logger or logging.getLogger(__name__)
        self.moderator = moderator  # Add the moderator as an attribute

    def check_consensus(self, game_state, current_player):
        """
        Checks for consensus among players using GPT as the primary detection method.
        """
        vote_counts = {}  # Initialize vote_counts to avoid unassigned variable error


        try:
            # Collect votes from werewolves
            werewolves = game_state.get_players_with_role("werewolf")
            for werewolf in werewolves:
                last_statement = game_state.players[werewolf]["last_statement"]
                target = self.extract_target_from_statement(last_statement)
                if target:
                    vote_counts[target] = vote_counts.get(target, 0) + 1

            if not vote_counts:
                self.logger.warning("No votes detected; skipping consensus check.")
                announcement = "No votes detected. Retrying consensus."
                self._log_announcement(announcement)
                return None

            # Build GPT prompt for consensus analysis
            prompt = self.prompt_builder.build_consensus_prompt(vote_counts)
            response = self.gpt_interaction.get_suggestion(prompt)
            print("\n--- GPT Consensus Analysis Response ---")
            print(response)

            # Parse GPT response for consensus
            if "Consensus reached on Player" in response:
                consensus_player = response.split("Player")[-1].strip()
                valid_targets = game_state.get_valid_targets(current_player)
                if consensus_player in valid_targets:
                    announcement = f"Player {consensus_player} has been eliminated during the night phase."
                    self._log_announcement(announcement)
                    print(f"\n*** Consensus reached on Player {consensus_player}! ***")
                    return consensus_player
                else:
                    print(f"Invalid consensus target: {consensus_player} (not a valid target).")

        except Exception as e:
            self.logger.error(f"Consensus check error: {e}")

        # Fallback for ties
        if vote_counts:
            max_votes = max(vote_counts.values(), default=0)
            candidates = [player for player, count in vote_counts.items() if count == max_votes]
            if len(candidates) == 1 and candidates[0] in game_state.get_valid_targets(current_player):
                announcement = f"Consensus fallback to Player {candidates[0]} due to highest votes."
                self._log_announcement(announcement)
                print(f"\n*** Consensus fallback to Player {candidates[0]} due to highest votes. ***")
                return candidates[0]

        announcement = "No consensus reached. Retrying."
        self._log_announcement(announcement)
        print("\nNo consensus reached. Multiple candidates tied or no votes cast.")
        return None

    def _log_announcement(self, announcement):
        """
        Logs an announcement using the moderator's global history.
        """
        if self.moderator and hasattr(self.moderator, 'global_history'):
            self.moderator.global_history.add_to_log("Moderator", announcement)
        else:
            self.logger.warning("Moderator or global history not properly initialized. Skipping log update.")

    @staticmethod
    def extract_target_from_statement(statement):
        """
        Extracts a target player from a given statement.
        """
        if not statement:
            return None
        for player_id in ["A", "B", "C", "D", "E", "Human"]:
            if player_id in statement:
                return player_id
        return None
