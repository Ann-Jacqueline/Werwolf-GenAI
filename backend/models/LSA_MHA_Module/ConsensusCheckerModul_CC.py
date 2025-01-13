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
        if self.global_history:
            self.global_history.record_event("announcement", {"text": announcement})
        else:
            self.logger.warning("Global history not properly initialized. Skipping log update.")

    def check_consensus(self, game_state, current_player):
        """
        Checks for consensus among players using GPT as the primary detection method.

        Args:
            game_state: The current game state.
            current_player: The player initiating the check.

        Returns:
            str or None: The player ID of the consensus target, or None if no consensus is reached.
        """
        try:
            # Retrieve the global conversation log
            conversation_log = game_state.global_conversation_log

            # Collect valid targets
            valid_targets = game_state.get_valid_targets(current_player)

            # Ensure conversation log is available
            if not conversation_log:
                self.logger.warning("No conversation log available for consensus analysis.")
                return None

            filtered_log = [
                (speaker, statement.strip())
                for speaker, statement in conversation_log
                if game_state.players.get(speaker, {}).get("remaining", False)
            ]

            # Build and send GPT prompt
            prompt = self.prompt_builder.build_consensus_prompt(filtered_log, valid_targets, game_state)

            # Log the consensus prompt in the game log
            self.logger.info(f"Generated Consensus Prompt:\n{prompt}")

            response = self.gpt_interaction.get_suggestion(prompt, valid_targets, game_state, current_player)

            # Log GPT response
            self.logger.info(f"GPT response: {response}")

            # Parse GPT response for consensus
            if "Consensus reached on Player" in response:
                consensus_player = response.split("Player")[-1].strip().replace('"', '').strip()
                if consensus_player in valid_targets:
                    return consensus_player

                # Retrieve the role of the eliminated player
                role = game_state.get_role(consensus_player) or "Unknown role"

                # Announce the elimination
                announcement = f"During the night, Player {consensus_player} ({role}) was eliminated by the werewolves."
                self._log_announcement(announcement)
                self.logger.info(announcement)

                return consensus_player

            # No consensus reached
            self.logger.info("No consensus reached.")
            return None

        except Exception as e:
            self.logger.error(f"Consensus check error: {e}")
            return None