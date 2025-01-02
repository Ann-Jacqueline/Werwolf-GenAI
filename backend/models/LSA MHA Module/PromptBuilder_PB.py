class PromptBuilder:
    """
    This class generates context-sensitive prompts for various phases of the Werewolf game.
    """

    @staticmethod
    def build_night_prompt(player, role, round_number, conversation_log, last_statement, valid_targets):
        """
        Generates a prompt for the night phase to select a player for elimination.

        Args:
            player (str): Player ID.
            role (str): Player's role.
            round_number (int): Current round number.
            conversation_log (str): Conversation log up to this point.
            last_statement (str): Player's last statement.
            valid_targets (list): List of valid targets for elimination.

        Returns:
            str: Formatted night phase prompt.
        """
        if not valid_targets:
            raise ValueError("No valid targets provided for elimination.")

        temporal_warning = (
            "Important: This is the first night of the game. "
            "You have no prior knowledge of events, roles, or behaviors. "
            "Make a decision based solely on logic or randomness, avoiding references to prior rounds, patterns, or player behavior."
        ) if round_number == 1 else ""

        return f"""
            === NIGHT PHASE (Round {round_number}) ===
            Player {player}, you are a {role} in the game of Werewolf.

            {temporal_warning}

            Last statement: '{last_statement or "None"}'
            Conversation so far:
            {conversation_log}

            Valid targets for elimination: {', '.join(valid_targets)}

            **Guidelines:**
            1. Acknowledge or challenge your teammate's suggestions if you have more information about player behaviour so not during the frist night of the first round.
            2. Propose an alternative target with reasoning or agree.
            3. Avoid suggesting the same target repeatedly without justification.
            4. Provide reasoning in one concise sentence ending with a period.
            5. Speak in the first person so ("I") and address your teammate personally with ("you")
            """

    @staticmethod
    def build_day_prompt(player, round_number, last_statement, conversation_log, role_strategy, remaining_players):
        """
        Generates a prompt for the day phase to support discussions and decisions.

        Args:
            player (str): Player ID.
            round_number (int): Current round number.
            last_statement (str): Player's last statement.
            conversation_log (str): Conversation log up to this point.
            role_strategy (str): Strategy specific to the player's role.
            remaining_players (list): List of remaining players.

        Returns:
            str: Formatted day phase prompt.
        """
        if not remaining_players:
            raise ValueError("No remaining players available for discussion.")

        return f"""
        === DAY PHASE (Round {round_number}) ===
        Player {player}, align with your strategy as a {role_strategy}.

        Last statement: '{last_statement or "None"}'
        Discussion log:
        {conversation_log or "No discussions yet."}

        Active players: {', '.join(remaining_players + ['Human Player'])}

        **Guidelines:**
        1. Respond concisely and reference prior statements from the log.
        2. React emotionally and offended if accused. Justify yourself persuasively and attempt to shift suspicion to others.
        3. Recognize when players try to deflect suspicion and address it based on your strategy.
        4. Suggest a target for elimination with a brief justification, swaying the conversation to align with your strategy.
        5. Respond only in one sentence!

        Example: "Player B appears suspicious based on their earlier statements. I recommend targeting them."
        """

    @staticmethod
    def build_vote_prompt(player, role, round_number, remaining_players):
        """
        Generates a prompt for the voting phase to cast an elimination vote.

        Args:
            player (str): Player ID.
            role (str): Player's role.
            round_number (int): Current round number.
            remaining_players (list): List of remaining players.

        Returns:
            str: Formatted voting phase prompt.
        """
        if not remaining_players:
            raise ValueError("No valid targets available for voting.")

        return f"""
        === VOTING PHASE (Round {round_number}) ===
        Player {player}, cast your vote as a {role}.

        Based on the discussions, choose one of the following players for elimination: {', '.join(remaining_players)}.

        Respond with the player's name only.

        Example: "Player A" 
        """


    def build_consensus_prompt(self, conversation_log, vote_counts):
        """
        Builds a prompt for consensus analysis.

        Args:
            conversation_log (list): Global conversation log.
            vote_counts (dict): Current vote tallies.

        Returns:
            str: A formatted prompt for GPT to analyze consensus.
        """
        log_entries = "\n".join([f"{speaker}: {statement}" for speaker, statement in conversation_log])
        vote_entries = "\n".join([f"Player {player}: {count} vote(s)" for player, count in vote_counts.items()])

        return f"""
        === CONSENSUS ANALYSIS ===
        Analyze the following conversation log to determine if consensus is reached:

        --- Current Conversation Log ---
        {log_entries}

        --- Current Vote Tallies ---
        {vote_entries}

        **Output Format:**
        1. Final consensus status: "Consensus reached on Player X" or "No consensus reached."

        Example:
        Consensus reached on Player A
        """

