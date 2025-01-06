import logging

class ConsensusChecker:
    """
    Checks for consensus among players using GPT and fallback mechanisms.
    """

    def __init__(self, gpt_interaction, prompt_builder, logger=None, moderator=None, global_history=None):
        """
        Initializes the ConsensusChecker.

        Args:
            gpt_interaction: Instance for interacting with GPT.
            prompt_builder: Instance for building GPT prompts.
            logger: Logger instance for logging information.
            moderator: Moderator instance for game coordination.
            global_history: Global history instance for recording game events.
        """
        self.gpt_interaction = gpt_interaction
        self.prompt_builder = prompt_builder
        self.logger = logger or logging.getLogger(__name__)
        self.moderator = moderator
        self.global_history = global_history

    @staticmethod
    def extract_target_from_statement(statement):
        """
        Extracts a target player from a given statement.
        Args:
            statement (str): The statement to parse for a target player.
        Returns:
            str or None: The target player ID if found, otherwise None.
        """
        if not statement:
            return None
        for player_id in ["A", "B", "C", "D", "E", "Human"]:
            if player_id in statement:
                return player_id
        return None

    def _log_announcement(self, announcement):
        """
        Logs an announcement using the moderator's global history or a fallback logger.
        Args:
            announcement (str): The announcement to log.
        """
        if self.moderator and hasattr(self.moderator, 'global_history'):
            self.moderator.global_history.add_to_log("Moderator", announcement)
        else:
            self.logger.warning("Moderator or global history not properly initialized. Skipping log update.")

    def check_consensus(self, game_state, current_player):
        """
        Checks for consensus among players using GPT as the primary detection method.

        Args:
            game_state: The current game state.
            current_player: The player initiating the check.

        Returns:
            str or None: The player ID of the consensus target, or None if no consensus is reached.
        """
        vote_counts = {}
        retry_limit = 3
        retries = 0

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
                self._log_announcement("No votes detected. Retrying consensus.")
                return None

            # Retrieve the global conversation log
            conversation_log = game_state.global_conversation_log

            # Debug vote_counts and conversation_log
            self.logger.debug(f"Vote counts: {vote_counts}")
            self.logger.debug(f"Conversation log: {conversation_log}")

            valid_targets = game_state.get_valid_targets(current_player)
            while retries < retry_limit:
                # Build and send GPT prompt
                prompt = self.prompt_builder.build_consensus_prompt(conversation_log, vote_counts)
                try:
                    response = self.gpt_interaction.get_suggestion(prompt)
                    self.logger.debug(f"GPT response: {response}")
                    print("\n--- GPT Consensus Analysis Response ---")
                    print(response)

                    # Parse GPT response for consensus
                    if "Consensus reached on Player" in response:
                        consensus_player = response.split("Player")[-1].strip()
                        if consensus_player in valid_targets:
                            announcement = f"Player {consensus_player} has been eliminated during the night phase."
                            self._log_announcement(announcement)
                            print(f"\n*** Consensus reached on Player {consensus_player}! ***")
                            return consensus_player
                        else:
                            self.logger.warning(f"Invalid consensus target: {consensus_player} (not a valid target).")
                except Exception as e:
                    self.logger.error(f"GPT interaction failed: {e}")
                    print(f"GPT interaction error during consensus check: {e}")  # Debug

                retries += 1

            # Fallback for highest votes
            max_votes = max(vote_counts.values(), default=0)
            candidates = [player for player, count in vote_counts.items() if count == max_votes]
            if len(candidates) == 1 and candidates[0] in valid_targets:
                announcement = f"Consensus fallback to Player {candidates[0]} due to highest votes."
                self._log_announcement(announcement)
                print(f"\n*** Consensus fallback to Player {candidates[0]} due to highest votes. ***")
                return candidates[0]

        except Exception as e:
            self.logger.error(f"Consensus check error: {e}")
            print(f"Consensus check error: {e}")  # Debug

        # No consensus reached after retries or fallback
        self._log_announcement("No consensus reached. Retrying.")
        print("\nNo consensus reached. Multiple candidates tied or no votes cast.")
        return None
