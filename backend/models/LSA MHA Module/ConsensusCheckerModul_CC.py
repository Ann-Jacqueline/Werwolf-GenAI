import logging



class ConsensusChecker:
    """
    Checks for consensus among players using GPT and fallback mechanisms.
    """

    def __init__(self, gpt_interaction, prompt_builder, logger=None):
        self.gpt_interaction = gpt_interaction
        self.prompt_builder = prompt_builder
        self.logger = logger or logging.getLogger(__name__)

    def check_consensus(self, game_state, current_player):
        """
        Checks for consensus among players using GPT as the primary detection method.
        """
        conversation_log = game_state.get_conversation_log()
        vote_counts = game_state.calculate_intermediate_votes()
        prompt = self.prompt_builder.build_consensus_prompt(conversation_log, vote_counts)

        try:
            response = self.gpt_interaction.get_suggestion(prompt)
            print("\n--- GPT Consensus Analysis Response ---")
            print(response)

            if "Consensus reached on Player" in response:
                consensus_player = response.split("Player")[-1].strip()
                valid_targets = game_state.get_valid_targets(current_player)
                if consensus_player in valid_targets:
                    print(f"\n*** Consensus reached on Player {consensus_player}! ***")
                    return consensus_player
                else:
                    print(f"Invalid consensus target: {consensus_player} (not a valid target).")
        except Exception as e:
            self.logger.error(f"Consensus check error: {e}")

        # Fallback mechanism for tied votes
        max_votes = max(vote_counts.values(), default=0)
        candidates = [player for player, count in vote_counts.items() if count == max_votes]

        if len(candidates) == 1 and candidates[0] in game_state.get_valid_targets(current_player):
            print(f"\n*** Consensus fallback to Player {candidates[0]} due to highest votes. ***")
            return candidates[0]

        print("\nNo consensus reached. Multiple candidates tied or no votes cast.")
        return None


