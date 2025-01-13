class PromptBuilder:
    """
    This class generates context-sensitive prompts for various phases of the Werewolf game.
    """

    def __init__(self, global_history=None):
        self.global_history = global_history

    @staticmethod
    def build_night_prompt(player, role, round_number, conversation_log, last_statement, valid_targets, game_state):
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

        remaining_targets = [target for target in valid_targets if game_state.players[target]["remaining"]]

        conversation_log = "\n".join(
            [f"{speaker}: {statement}" for speaker, statement in game_state.night_log]
        )

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

            Valid targets for elimination: {', '.join(remaining_targets)}

            **Guidelines:**
            1. Acknowledge or challenge your teammate's suggestions if you have more information about player behaviour. During the first night of the first round don't make assumptions based on prior events.
            2. Be agreeable with your teammate's suggestion unless you have a founded strategic reason to propose an alternative.
            3. Clearly explain your choice of target based on:
               - Statements from the conversation log.
               - The strategic value of eliminating the target (e.g., a special role or an active participant).
            4. Do not suggest the same target repeatedly without adding new reasoning or strengthening your case. 
            5. Provide reasoning in one concise sentence ending with a period.
            6. Speak in the first person about yourself/ player-id, so ("I") and ("me") and address your teammate personally with ("you")
            """

    def build_day_prompt(self, player_id, round_number, game_state):
        """
        Builds the prompt for the day phase of the game for a specific player.

        Args:
            player_id (str): The player for whom the prompt is built.
            round_number (int): The current round number.
            game_state (GameState): The game state instance containing all player data.

        Returns:
            str: A structured prompt for GPT.
        """
        player_state = game_state.players[player_id]

        remaining_players = [
            p for p in game_state.get_remaining_players()  # #UPDATE!! Use global remaining_players from game state
            if p != player_id  # Exclude the current player
        ]

        # Debug: Ensure no player is missing
        if not remaining_players:
            raise ValueError(f"No remaining players found for Player {player_id}. This might indicate an issue.")

        # Use only day phase logs
        discussion_log = "\n".join(
            [f"{speaker}: {statement}" for speaker, statement in game_state.players[player_id]["conversation_log"]]
        )

        return f"""
        === DAY PHASE (Round {round_number}) ===
        Player {player_id}, you are a {player_state["role"]} in the game of Werewolf. Your strategy is:
        {player_state["base_strategy"]}

        Here is your memory; it is your individual game state:
        --- Player State ---
        Role: {player_state["role"]}
        Awake: {'Yes' if player_state["awake"] else 'No'}
        Remaining: {'Yes' if player_state["remaining"] else 'No'}
        Remaining Players: {', '.join(remaining_players)}
        Last Statement: '{player_state["last_statement"] or "None"}'

        Here is what has been said so far:
        --- Discussion Log ---
        {discussion_log}

        **Guidelines:**
        1. Respond directly to the Human's latest statement if relevant. Always treat the Human Player same to the others.
        2. React emotionally and persuasively if accused, and attempt to shift suspicion to others.
        3. Reference the discussion log and align your response with your strategy.
        4. Provide a clear argument with reasoning for targeting a specific player for elimination:
       - Reference behavior or statements from the discussion log. Do not reveal what was said in the night phase. 
       - Observable behavior of players.
       - Align your response with your role's strategy.
       - Do not suggest already eliminated players!
       - Be persuasive, concise, and logical.
        5. Focus your suspicion on one target and avoid contradictory accusations.
        6. Do not disclose or speculate on knowledge that was private to specific roles during the night. 
        7. Respond concisely always in one full sentence! Speak in a natural and conversational tone.
        8. If you are a werewolf, prioritize targeting non-werewolves to ensure your survival and game victory. 
        Do not accuse your teammate(s)/ the other werewolves! Do not reveal what you discussed and voted with you teammate in the nightphase.


        Example: "Player B appears suspicious based on their earlier statements. I recommend targeting them."
        """

    @staticmethod
    def build_agent_vote_prompt(player, role, round_number, remaining_players, game_state):
        """
        Generates a prompt for an agent to cast a vote during the voting phase.

        Args:
            player (str): Player ID.
            role (str): Player's role.
            round_number (int): Current round number.
            remaining_players (list): List of remaining players.
            game_state (GameState): The current game state.


        Returns:
            str: Formatted voting phase prompt for agents.
        """

        # Filter out eliminated players to ensure valid targets
        valid_targets = [p for p in remaining_players if game_state.players[p]["remaining"]]

        if not valid_targets:
            raise ValueError("No valid targets available for voting.")

        # Role-specific voting strategy
        if role == "werewolf":
            strategy_instruction = (
                "As a werewolf, prioritize targeting non-werewolves to ensure your survival and victory. "
                "Do not vote for your teammate(s)."
            )
        else:
            strategy_instruction = (
                "Vote based on your analysis of discussions and observations. Remember, you are trying to find and eliminate a werewolf."
                "Consider the behavior and statements of the remaining players."
            )

        return f"""
        === VOTING PHASE (Round {round_number}) ===
        Player {player}, cast your vote as a {role}.
        
        {strategy_instruction}

        Based on the discussions, choose one of the following players for elimination: {', '.join(remaining_players)}.
        Only consider the following valid targets for elimination: {', '.join(valid_targets)}.
        Do not use information that you would not logically know from the game so far.


        Respond with the player's name only.

        Example: "Player A" 
        """

    @staticmethod
    def build_vote_analysis_prompt(conversation_log, valid_targets, game_state):
        """
        Builds a prompt for vote analysis to determine the eliminated player.

        Args:
            conversation_log (list): The conversation log for context.
            valid_targets (list): List of valid targets for elimination.
            game_state (GameState): The current game state.

        Returns:
            str: A structured prompt for GPT to analyze votes and determine the eliminated player.
        """

        valid_targets = [
            player_id for player_id in game_state.get_remaining_players()  # #UPDATE!!
            if game_state.players[player_id]["remaining"]
        ]

        log_entries = "\n".join([f"{speaker}: {statement}" for speaker, statement in conversation_log])

        roles_info = "\n".join(
            [f"Player {player}: {game_state.get_role(player)}" for player in valid_targets]
        )

        return f"""
        === VOTE ANALYSIS ===
        Analyze the voting process to determine the eliminated player.

        --- Current Conversation Log ---
        {log_entries}

        --- Valid Targets for Elimination ---
        {', '.join(valid_targets)}

        --- Player Roles ---
        {roles_info}

        **Task:**
        1. Review the conversation log to identify votes cast by each player.
        2. Count the votes for each valid target.
        3. Determine the player with the most votes.
        4. If there is a tie, randomly select one of the tied players as the eliminated player.
        5. Only consider targets listed above as valid for elimination.

        Example Output:
        Consensus reached on Player B
        """

    def build_consensus_prompt(self, conversation_log, valid_targets, game_state):
        """
        Builds a prompt for consensus analysis.

        Args:
            conversation_log (list): Global conversation log.
            valid_targets (list): List of valid targets for elimination.

        Returns:
            str: A formatted prompt for GPT to analyze consensus.
        """
        # Format the conversation log
        log_entries = "\n".join([f"{speaker}: {statement}" for speaker, statement in conversation_log])

        # Format the list of valid targets
        valid_targets = [target for target in valid_targets if game_state.players[target]["remaining"]]
        target_list = ", ".join(f"Player {target}" for target in valid_targets)

        return f"""
        === CONSENSUS ANALYSIS ===
        You are analyzing the game state to determine if the players have reached a consensus on who to target.

        --- Current Conversation Log ---
        {log_entries}

        --- Valid Targets for Elimination ---
        {', '.join(valid_targets)}

        **Task:**
        1. Review the conversation log carefully to identify mentions of potential elimination targets.
        2. Identify agreement statements (e.g., "I agree with Player X about targeting Player Y").
        3. Determine if a consensus exists based on the players consistently agreeing on one target.
        4. Only consider targets listed above as valid for elimination. No players eliminated in other phases.
        5. If multiple players align on the same valid target, declare "Consensus reached on Player X" (replace X with the player ID).
        6. If no agreement exists or the discussion is split between multiple targets, declare "No consensus reached."

        **Examples:**
        - If Player B suggests targeting Player D, and Player C explicitly agrees, the output should be:
          "Consensus reached on Player D."
        - If Player B suggests Player D, and Player C disagrees or suggests another target, the output should be:
          "No consensus reached."

        **Output Format:**
        Final consensus status: "Consensus reached on Player X" or "No consensus reached."

        Example Output:
        Consensus reached on Player D
        """