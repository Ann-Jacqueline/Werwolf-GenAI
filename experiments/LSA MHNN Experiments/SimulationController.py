"""
SimulationController.py - Simulations-Experiment für Nacht- und Tagphasen

Der Controller steuert die verschiedenen Phasen des Spiels, einschließlich der Nacht- und Tagphasen,
und koordiniert die Interaktionen zwischen den Spielern, der KI und dem menschlichen Spieler.
"""
import random
import os
import logging
import re
import time


from openai import OpenAI
from GameStateModul import GameState  # Import the GameState class


class SimulationController:
    """
    Die SimulationController-Klasse verwaltet die Spielmechanik und Spielzustände.
    """
    def __init__(self):
        """
        Initialisiert den SimulationController.
        Konfiguriert das Logging, lädt den API-Schlüssel, initialisiert den OpenAI-Client und den persistenten Spielzustand.
        """
        # Configure logging
        logging.basicConfig(
            filename="game_log.txt",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

        # Load API key from environment variable
        self.api_key = os.getenv("YOUR_API_KEY")
        if not self.api_key:
            raise ValueError("Environment variable 'YOUR_API_KEY' is not set!")

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

        # Initialize game states for players A to E
        self.agent_game_states = {chr(65 + i): GameState() for i in range(5)}
        self.round_number = 1

    def set_all_awake_status(self, status: bool):
        """
        Updates the 'awake' status for all players in the game.

        Args:
            status (bool): True for active players, False otherwise.
        """
        for player, state in self.agent_game_states.items():
            state.set_awake(status)
        self.logger.info(f"All players set to awake: {status}")

    def initialize_roles(self):
        """
        Mischt die Rollen der Spieler (Werwolf, Dorfbewohner, Seher) zufällig und ordnet sie den Spielern zu.
        """
        roles = ['villager', 'villager', 'seer', 'werewolf', 'werewolf']
        random.shuffle(roles)

        for i, player in enumerate(self.agent_game_states.keys()):
            self.agent_game_states[player].update_role_and_strategy(roles[i])
            self.agent_game_states[player].remaining_players = list(self.agent_game_states.keys())

        print("Roles initialized:")
        for player, state in self.agent_game_states.items():
            print(f"Player {player}: {state.role} with strategy: {state.base_strategy}")

    def log_game_state(self):
        """
        Protokolliert den aktuellen Spielzustand, einschließlich Spieler, Rollen und Geschichte.
        """
        for player, state in self.agent_game_states.items():
            self.logger.info(f"Player {player} Game State: {state.to_dict()}")
            print(f"Player {player} Game State: {state.to_dict()}")

    def get_gpt_suggestion(self, agent, context):
        """
        Requests a GPT suggestion for a given agent based on context.
        Validates the suggestion and ensures it aligns with the game rules, including strategy enforcement for roles.
        If the suggestion is invalid, GPT is reprompted up to a maximum number of attempts.
        """

        import random

        max_attempts = 3  # Maximum number of attempts to get a valid response
        attempts = 0

        while attempts < max_attempts:
            try:
                # GPT call
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": context}]
                )
                suggestion = response.choices[0].message.content.strip()

                # Log the prompt and response
                self.logger.info(f"Prompt for Player {agent}: {context.strip()}")
                self.logger.info(f"Response Player {agent}: {suggestion}")

                # Access the game state for the specific agent
                state = self.agent_game_states[agent]

                # Include "Human Player" in valid targets
                valid_targets = state.remaining_players + ["Human Player"]
                if state.role == "werewolf":
                    # Werewolves must avoid voting for allies
                    valid_targets = [
                                        p for p in state.remaining_players
                                        if self.agent_game_states[p].role != "werewolf"
                                    ] + ["Human Player"]

                # Relaxed Validation:
                # 1. Ensure suggestion includes a valid target.
                # 2. Allow concise responses like "C" or "Player C."
                if not any(
                        f"Player {p}" in suggestion or suggestion == p
                        for p in valid_targets
                ):
                    self.logger.warning(f"Invalid target from Player {agent}: {suggestion}")
                else:
                    # Valid suggestion
                    state.conversation_log.append((agent, suggestion))
                    state.last_statement = suggestion
                    print(f"Response from {agent}: {suggestion}")
                    self.log_game_state()
                    return suggestion

                # If invalid, increment attempts and reprompt
                attempts += 1
                print(f"Reprompting GPT for Player {agent} (Attempt {attempts}/{max_attempts})...")

            except Exception as e:
                self.logger.error(f"Error during GPT call for Player {agent}: {e}")
                print(
                    f"Error encountered for Player {agent}: {str(e)}. Retrying... (Attempt {attempts + 1}/{max_attempts})")
                attempts += 1

        # Fallback logic if all attempts fail
        fallback_suggestion = random.choice(valid_targets)
        print(f"Fallback suggestion for Player {agent}: Player {fallback_suggestion}")
        self.logger.error(f"Failed to get a valid response from Player {agent} after {max_attempts} attempts.")
        return f"Player {fallback_suggestion}"

    def build_prompt(self, agent):
        """
        Creates a GPT prompt for the given agent, incorporating their last suggestion and conversation history.
        Adds warnings for temporal consistency if it's the first round and night phase.
        """
        # Access the specific agent's game state
        state = self.agent_game_states[agent]

        role = state.role
        last_statement = state.last_statement or "None"
        conversation_log = (
            "\n".join([f"{speaker}: {statement}" for speaker, statement in state.conversation_log])
            if state.conversation_log else "No previous conversation."
        )

        # Adding temporal consistency instruction for round 1, night 1
        temporal_warning = ""
        if self.round_number == 1 and self.is_night_phase():
            temporal_warning = (
                "Important: This is the first night of the game. You have no prior knowledge of events, roles, or behaviors. "
                "Make a decision based solely on logic or randomness, avoiding references to prior rounds, patterns, or player behavior."
            )

        valid_targets = ", ".join(self.get_valid_targets())

        return f"""
            You are Player {agent}, a {role} in the game of Werewolf.
            It is the night phase of round {self.round_number}.
            Discuss with your teammate and suggest a villager to eliminate.

            {temporal_warning}

            Your last statement: '{last_statement}'
            Conversation so far:
            {conversation_log}

            **Guidelines for your response:**
            1. Engage with your teammate's suggestion: Acknowledge their points and respond directly.
            2. Suggest a villager to eliminate from: {valid_targets}.
            3. Provide reasoning in one concise sentence ending with a period.
            4. Do not ask questions or leave decisions open-ended.
            5. Avoid repetitive or irrelevant responses.

            Example Response: "I agree that Player A is a strategic risk due to their alliances, so I suggest targeting them."
        """

    def is_night_phase(self):
        """
        Überprüft, ob sich das Spiel in der Nachtphase befindet.
        """
        return self.round_number % 2 == 1

    def get_valid_targets(self):
        """
        Gibt eine Liste gültiger Ziele zurück, die eliminiert werden können (keine Werwölfe).
        """
        valid_targets = []
        for player, state in self.agent_game_states.items():
            if state.role != 'werewolf' and player in state.remaining_players:
                valid_targets.append(player)
        return valid_targets

    def log_vote(self, voter, target):
        """
        Logs a vote for elimination in the game state.
        """
        if voter in self.agent_game_states and target in self.agent_game_states:
            self.agent_game_states[voter].track_vote(voter, target)

    def log_agreement(self, supporter, target):
        """
        Logs an agreement with targeting in the game state.
        """
        if supporter in self.agent_game_states and target in self.agent_game_states:
            self.agent_game_states[supporter].track_agreement(supporter, target)

    def check_for_consensus_gpt(self):
        """
        Überprüft mithilfe von GPT, ob Konsens unter den Spielern erreicht wurde.
        - Analysiert das Gesprächsprotokoll.
        - Benutzt einen Vote Counter (Tallies) um die zwischenzeitigen Eliminierungen zu zählen
        - Gibt die Zielperson zurück, wenn Konsens erreicht wurde, oder None, wenn nicht.
        """
        from collections import Counter

        # Aggregate and clean conversation logs from all GameStates
        conversation_log = [
            f"{speaker}: {statement}"
            for state in self.agent_game_states.values()
            for speaker, statement in state.conversation_log
        ]
        unique_log = list(dict.fromkeys(conversation_log))  # Remove duplicate entries

        # Initialize vote and agreement tallies
        vote_tallies = Counter()
        agreements = Counter()

        # Extract votes and agreements from the logs
        for entry in unique_log:
            if "votes to eliminate Player" in entry:
                voter, statement = entry.split(": ", 1)
                target = statement.split("votes to eliminate Player")[-1].strip()
                vote_tallies[target] += 1
            elif "agrees with targeting Player" in entry:
                supporter, statement = entry.split(": ", 1)
                target = statement.split("agrees with targeting Player")[-1].strip()
                agreements[target] += 1

        # Display current vote tallies and agreements
        print("\n--- Current Vote Tallies ---")
        for target, count in vote_tallies.items():
            print(f"Player {target}: Voted by {count} players")

        print("\n--- Current Explicit Agreements ---")
        for target, count in agreements.items():
            print(f"Player {target}: Agreed by {count} players")

        # Check for consensus (majority vote)
        total_players = len(self.agent_game_states)
        for target, count in vote_tallies.items():
            if count > total_players // 2:  # Simple majority
                print(f"\n*** Consensus detected on Player {target}! ***")
                return target

        # Fall back to GPT analysis for further insights
        try:
            prompt = (
                f"Analyze the conversation log to determine if consensus is reached on a target for elimination. "
                f"Follow this format:\n\n"
                f"--- Current Vote Tallies ---\n"
                f"Player <Target>: Voted by [List of unique voters] (Total votes: X)\n\n"
                f"--- Current Explicit Agreements ---\n"
                f"Player <Target>: Agreed by [List of unique supporters] (Total agreements: X)\n\n"
                f"Consensus Check Status: <Consensus reached on Player X | No consensus reached>\n\n"
                f"Conversation Log:\n{unique_log}"
            )
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt}]
            )
            gpt_response = response.choices[0].message.content.strip()

            # Parse GPT response for consensus
            consensus_match = re.search(r"Consensus reached on Player ([A-E])", gpt_response)
            if consensus_match:
                consensus_player = consensus_match.group(1)
                print(f"\n*** Consensus detected by GPT on Player {consensus_player}! ***")
                return consensus_player

            print("No consensus reached yet (GPT analysis).")
            return None
        except Exception as e:
            self.logger.error(f"Error during consensus check with GPT: {e}")
            return None

    def calculate_intermediate_votes(self):
        """
        Berechnet Zwischenstände der Stimmen basierend auf dem Gesprächsprotokoll.
        Gibt ein Dictionary mit den Stimmen für jede Zielperson zurück.
        """
        # Aggregate logs from all GameStates
        aggregated_conversation_log = [
            (speaker, statement)
            for state in self.agent_game_states.values()
            for speaker, statement in state.conversation_log
        ]

        # Initialize votes for players A to E
        votes = {chr(65 + i): 0 for i in range(5)}

        # Count votes from the aggregated conversation log
        for _, statement in aggregated_conversation_log:
            for player in votes.keys():
                if f"Player {player}" in statement:
                    votes[player] += 1

        return votes

    def fallback_elimination(self):
        """
        Wählt ein Ziel zur Eliminierung basierend auf dem häufigsten Vorkommen im Gesprächsprotokoll,
        falls kein Konsens erreicht wird.
        """
        valid_targets = self.get_valid_targets()
        if not valid_targets:
            return None

        # Aggregate conversation logs from all GameStates
        aggregated_conversation_log = [
            statement
            for state in self.agent_game_states.values()
            for _, statement in state.conversation_log
        ]

        # Determine the target with the most mentions
        return max(
            valid_targets,
            key=lambda target: sum(target in statement for statement in aggregated_conversation_log),
            default=None
        )

    def finalize_elimination(self, eliminated_player):
        """
        Finalisiert die Eliminierung eines Spielers:
        - Entfernt den Spieler aus der Liste der verbleibenden Spieler in allen GameStates.
        - Aktualisiert den Spielverlauf in jedem betroffenen GameState.
        - Protokolliert die Entscheidung.
        """
        player_found = False

        for player, state in self.agent_game_states.items():
            if eliminated_player in state.remaining_players:
                state.remove_player(eliminated_player)
                player_found = True

        if player_found:
            print(f"Final Decision: Player {eliminated_player} eliminated.")
            self.logger.info(f"Final Decision: Player {eliminated_player} eliminated.")

            # Deactivate the eliminated player's state
            if eliminated_player in self.agent_game_states:
                eliminated_state = self.agent_game_states[eliminated_player]
                eliminated_state.awake = False
                eliminated_state.remaining_players = []
                eliminated_state.conversation_log = []

            # Log elimination in all game states
            summary = {
                "round_number": self.round_number,
                "phase": "night" if self.round_number % 2 == 1 else "day",
                "summary": f"Player {eliminated_player} was eliminated."
            }
            for state in self.agent_game_states.values():
                state.conversation_log.append(("Moderator", summary["summary"]))

        else:
            print("Error: Eliminated player not found in remaining players.")
            self.logger.error("Error: Eliminated player not found in remaining players.")

    def handle_night_phase(self):
        """
        Handhabt die Nachtphase des Spiels:
        - Fordert Vorschläge der Werwölfe an.
        - Überprüft nach jedem Vorschlag auf Konsens.
        - Finalisiert die Eliminierung einer Zielperson.
        - Übergang zur Tagphase.
        """
        print("Night phase started.")

        # Identify werewolves based on their roles
        werewolves = [
            player for player, state in self.agent_game_states.items()
            if state.role == 'werewolf'
        ]

        eliminated_player = None
        timeout = 10  # Maximum attempts to reach consensus
        attempts = 0

        while not eliminated_player and attempts < timeout:
            for werewolf in werewolves:
                state = self.agent_game_states[werewolf]
                prompt = self.build_prompt(werewolf)
                suggestion = self.get_gpt_suggestion(werewolf, prompt)

                # Add the suggestion to the conversation log
                if suggestion:
                    state.add_to_conversation_log(werewolf, suggestion)

                # Print current game state for debugging
                print("\nCurrent Game State for Werewolf Discussion:")
                print(f"Remaining Players: {state.remaining_players}")
                print(f"Conversation Log: {state.conversation_log}")


                eliminated_player = self.check_for_consensus_gpt()

                if eliminated_player:
                    break

            # Increment attempts
            attempts += 1

        # If no consensus is reached after timeout, use fallback elimination
        if not eliminated_player:
            print("Timeout reached. Using fallback elimination.")
            eliminated_player = self.fallback_elimination()

        # Finalize elimination and proceed to day phase
        if eliminated_player:
            self.finalize_elimination(eliminated_player)
            self.handle_day_phase(eliminated_player)
        else:
            print("No valid player eliminated during the night phase.")
            self.logger.warning("No valid player eliminated during the night phase.")

    def handle_day_phase(self, eliminated_player):
        """
        Handles the day phase of the game:
        - Announces the player eliminated during the night.
        - Facilitates structured turn-based discussion and time-limited debate.
        - Initiates the voting phase when the human player decides to vote.
        """
        print("Day phase triggered.")
        self.logger.info("Day phase triggered.")

        # Moderator announces the eliminated player and their role
        eliminated_role = self.agent_game_states[eliminated_player].role
        moderator_announcement = f"The moderator announces: During the night phase, Player {eliminated_player} ({eliminated_role}) was eliminated."
        print(moderator_announcement)
        self.logger.info(moderator_announcement)

        for state in self.agent_game_states.values():
            state.add_to_conversation_log("Moderator", moderator_announcement)

        discussion_ongoing = True
        while discussion_ongoing:
            start_time = time.time()

            while time.time() - start_time < 180:  # 3-minute timer
                # Human player's input
                human_input = input("Human Player: ").strip()
                if human_input:
                    for state in self.agent_game_states.values():
                        state.add_to_conversation_log("Human", human_input)
                    self.logger.info(f"Human Player: {human_input}")

                # Continue to agent responses even if no input is provided
                for player, state in self.agent_game_states.items():
                    if player in state.remaining_players:
                        conversation_log = "\n".join(
                            [f"{speaker}: {statement}" for speaker, statement in state.conversation_log[-5:]]
                        )  # Last 5 statements for context
                        context = f"""
                        You are Player {player}, a {state.role} in the game of Werewolf. It is the day phase of round {self.round_number}.
                        Your role strategy is: {state.base_strategy}
                        Your last input was: '{state.last_statement or "None"}'.
                        Here's the recent discussion log:
                        {conversation_log}

                        Guidelines for your response:
                        1. Respond concisely (in one line) and reference at least one prior statement or argument made in the discussion log.
                        2. Align your argument with your role's strategy ({state.base_strategy}).
                        3. Build on or challenge the suggestions made by others.
                        4. Refer only to active players or the 'Human Player': {', '.join(state.remaining_players + ["Human Player"])}.
                        5. Suggest a target for elimination and provide reasoning.

                        Remember, your response must engage with ongoing discussion and be tailored to the recent context.
                        """
                        suggestion = self.get_gpt_suggestion(player, context)
                        if suggestion:
                            print(f"{player}: {suggestion}")
                            state.add_to_conversation_log(player, suggestion)
                            self.logger.info(f"{player}: {suggestion}")

            # Moderator intervention after the time limit
            print("\n--- Moderator: Time is up for this phase ---")
            continue_discussion = input(
                "Do you want to continue discussing or proceed to voting? (continue/vote): ").strip().lower()

            if continue_discussion == "continue":
                print("\nThe discussion phase will continue. The timer has been reset.")
                self.logger.info("Human Player chose to continue the discussion phase.")
                continue  # Reset the timer by restarting the loop
            elif continue_discussion == "vote":
                print("\nThe discussion phase has ended. Proceeding to the voting phase.")
                self.logger.info("Human Player chose to proceed to the voting phase.")
                discussion_ongoing = False
            else:
                print("Invalid input. Assuming you want to continue discussing.")
                self.logger.warning("Invalid input during continue/vote prompt. Defaulting to continue.")
                continue  # Reset the timer by restarting the loop

        # Proceed to voting phase
        self.vote_phase()

    def vote_phase(self):
        """
        Facilitates the voting phase where each player, including the human player, casts a vote for elimination.
        Collects votes and resolves the outcome.
        """
        print("\n--- Final Voting ---")
        print("Each player will now cast their vote for elimination.")

        votes = {}

        # AI players cast their votes
        for player, state in self.agent_game_states.items():
            if player in state.remaining_players:
                context = f"""
                You are Player {player}, a {state.role} in the game of Werewolf. It is the final voting phase of round {self.round_number}.
                Based on the discussion so far, cast your vote for elimination. Choose one of the remaining players: {', '.join(state.remaining_players)}.
                Your response must be in one concise line and only name one valid player.
                """
                vote = self.get_gpt_suggestion(player, context)
                if vote:
                    print(f"{player} votes to eliminate: {vote}")
                    votes[player] = vote
                    self.logger.info(f"{player} votes for: {vote}")

        # Human player casts their vote
        valid_targets = [p for p in self.agent_game_states if p in self.agent_game_states[p].remaining_players]
        human_vote = None
        while human_vote not in valid_targets:
            print(
                f"Moderator: Human Player, cast your vote for elimination. Valid options are: {', '.join(valid_targets)}.")
            human_vote = input("Human Player: ").strip()
            if human_vote not in valid_targets:
                print("Invalid vote. Please choose a valid player.")

        print(f"Human Player votes to eliminate: {human_vote}")
        votes["Human Player"] = human_vote
        self.logger.info(f"Human Player votes for: {human_vote}")

        # Resolve votes
        self.resolve_votes(votes)

    def resolve_votes(self, votes):
        """
        Resolves the voting phase by tallying votes and determining the elimination outcome.
        - Tallies votes for each player.
        - Determines the player with the most votes for elimination.
        - Handles ties by randomly selecting among tied candidates.
        - Finalizes the elimination and logs results.
        """
        print("\n--- Voting Results ---")
        self.logger.info("Tallying votes.")

        # Tally votes
        vote_counts = {}
        for vote in votes.values():
            vote_counts[vote] = vote_counts.get(vote, 0) + 1

        # Display vote counts
        for player, count in vote_counts.items():
            print(f"Player {player}: {count} votes")
            self.logger.info(f"Player {player}: {count} votes")

        # Determine the outcome
        if vote_counts:
            max_votes = max(vote_counts.values())
            candidates = [player for player, count in vote_counts.items() if count == max_votes]

            if len(candidates) == 1:
                eliminated = candidates[0]
                print(f"\nPlayer {eliminated} is eliminated with {max_votes} votes.")
                self.logger.info(f"Player {eliminated} is eliminated with {max_votes} votes.")
            else:
                print("\nNo consensus reached. A random player from the tied candidates will be eliminated.")
                eliminated = random.choice(candidates)
                print(f"Player {eliminated} is randomly eliminated.")
                self.logger.info(f"Player {eliminated} is randomly eliminated.")

            # Finalize the elimination
            self.finalize_elimination(eliminated)
        else:
            print("No votes were cast. No player is eliminated.")
            self.logger.info("No votes were cast. No player is eliminated.")

    def get_last_eliminated_player(self):
        """
        Retrieves the most recently eliminated player based on the conversation logs.
        Scans through the moderator announcements across all GameState logs.
        """
        for state in self.agent_game_states.values():
            for speaker, statement in reversed(state.conversation_log):
                if speaker == "Moderator" and "was eliminated" in statement:
                    match = re.search(r"Player ([A-E])", statement)
                    if match:
                        return match.group(1)
        return None  # No elimination found

    def handle_phase(self):
        """
        Schaltet zwischen Nacht- und Tagphasen und führt die entsprechende Logik aus.
        """
        if self.round_number % 2 == 1:  # Nachtphase
            print(f"Starting Night Phase for Round {self.round_number}")
            self.handle_night_phase()
        else:  # Tagphase
            print(f"Starting Day Phase for Round {self.round_number}")

            # Retrieve the last eliminated player for the day phase
            eliminated_player = self.get_last_eliminated_player()
            if eliminated_player:
                self.handle_day_phase(eliminated_player)
            else:
                print("No player eliminated in the previous night phase.")

    def start_game(self):
        """
        Startet das Spiel:
        - Initialisiert die Rollen.
        - Beginnt mit der Nachtphase.
        """
        print("Game started!")
        self.initialize_roles()
        self.handle_night_phase()


# Example usage:
if __name__ == "__main__":
    controller = SimulationController()
    controller.start_game()