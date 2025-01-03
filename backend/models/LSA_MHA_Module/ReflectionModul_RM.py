class Reflection:
    """
    Das Reflection-Modul bietet Funktionen zur Unterstützung von Agentenreflexion und Analyse latenter Zustände.
    """

    def __init__(self, game_state, global_history=None):
        """
        Initialisiert das Modul mit dem aktuellen Spielzustand.

        Args:
            game_state (dict): Der globale Spielzustand (player_id -> GameState).
            global_history (GlobalHistoryModel): Optional, um Reflexionsergebnisse aufzuzeichnen.
        """
        self.game_state = game_state
        self.global_history = global_history

    def get_strategy(self, role, phase=None):
        """
        Gibt die Strategie basierend auf der Rolle und optional der Phase zurück.

        Args:
            role (str): Die Rolle des Spielers.
            phase (str, optional): Die Phase des Spiels (z. B. 'day' oder 'night').

        Returns:
            str: Die Strategie für die Rolle.
        """
        strategies = {
            "villager": {
                "default": "Focus on gathering information and identifying suspicious behavior."
            },
            "werewolf": {
                "default": "Deflect suspicion, manipulate discussions, and work with your ally to eliminate threats."
            },
            "seer": {
                "default": "Provide subtle hints about suspicions without revealing your role prematurely.",
                "day": "Share insights cautiously to avoid detection."
            }
        }
        if phase and phase in strategies.get(role, {}):
            return strategies[role][phase]
        return strategies.get(role, {}).get("default", "Play according to the current game context.")

    def get_all_strategies(self):
        """
        Gibt alle Strategien für alle Rollen zurück.

        Returns:
            dict: Ein Dictionary mit Rollen als Schlüssel und Strategien als Werte.
        """
        return {
            "villager": "Focus on gathering information and identifying suspicious behavior.",
            "werewolf": "Deflect suspicion, manipulate discussions, and work with your ally to eliminate threats.",
            "seer": "Provide subtle hints about suspicions without revealing your role prematurely."
        }

    def reflect(self, player, round_number, phase):
        """
        Generiert eine Reflexion für einen bestimmten Spieler basierend auf dem Spielverlauf.

        Args:
            player (str): Die Spielerkennung.
            round_number (int): Die aktuelle Runde.
            phase (str): Die Phase (z. B. "night" oder "day").

        Returns:
            dict: Reflexionsdaten für den Spieler.
        """
        if player not in self.game_state:
            raise ValueError(f"Player {player} not found in game state.")

        state = self.game_state[player]
        reflection_data = {
            "phase": phase,
            "round_number": round_number,
            "player": player,
            "remaining_players": state.get('remaining_players', []),
            "last_statement": state.get('last_statement', None),
            "role": state.get('role', None),
            "strategy": self.get_strategy(state.get('role', "unknown"), phase)
        }

        # Optional: Log reflection data
        if self.global_history:
            self.global_history.record_event("player_reflection", reflection_data)

        return reflection_data

    def analyze_latent_states(self):
        """
        Analysiert latente Zustände (z. B. Vertrauen, Allianzen) im Spielverlauf.

        Returns:
            dict: Eine Zusammenfassung latenter Zustände für alle Spieler.
        """
        latent_states = {}
        for player_id, state in self.game_state.items():
            trust = self._calculate_trust(state)
            latent_states[player_id] = {
                "trust": trust,
                "alliances": self._detect_alliances(player_id, trust),
                "suspicion": self._calculate_suspicion(state)
            }

        # Optional: Log latent state analysis
        if self.global_history:
            self.global_history.record_event("latent_state_analysis", latent_states)

        return latent_states

    def _calculate_trust(self, state):
        """
        Berechnet das Vertrauen eines Spielers basierend auf den Interaktionen.

        Args:
            state (dict): Der Zustand des Spielers.

        Returns:
            float: Ein Wert, der das Vertrauen widerspiegelt (z. B. 0-1).
        """
        positive_mentions = sum(1 for log in state.get('conversation_log', []) if "agrees" in log)
        return positive_mentions / max(len(state.get('conversation_log', [])), 1)

    def _calculate_suspicion(self, state):
        """
        Berechnet das Misstrauen eines Spielers.

        Args:
            state (dict): Der Zustand des Spielers.

        Returns:
            float: Ein Wert für Misstrauen (z. B. 0-1).
        """
        negative_mentions = sum(1 for log in state.get('conversation_log', []) if "votes to eliminate" in log)
        return negative_mentions / max(len(state.get('conversation_log', [])), 1)

    def _detect_alliances(self, player_id, trust):
        """
        Erkennt potenzielle Allianzen basierend auf Vertrauen und Gesprächsverlauf.

        Args:
            player_id (str): Die Spielerkennung.
            trust (float): Der berechnete Vertrauenswert.

        Returns:
            list: Eine Liste potenzieller Allianzen.
        """
        if trust > 0.5:  # Schwellenwert für Vertrauen
            return [other_id for other_id in self.game_state if other_id != player_id]
        return []

    def check_temporal_consistency(self, player, phase, round_number):
        """
        Überprüft die Konsistenz der Aussagen eines Spielers mit der aktuellen Phase und Runde.

        Args:
            player (str): Die Spielerkennung.
            phase (str): Die Phase des Spiels (z. B. "night" oder "day").
            round_number (int): Die aktuelle Runde.

        Returns:
            bool: True, wenn die Aussagen konsistent sind, sonst False.
        """
        if player not in self.game_state:
            raise ValueError(f"Player {player} not found in game state.")

        state = self.game_state[player]
        for log in state.get('conversation_log', []):
            if round_number == 1 and phase == "night" and "prior knowledge" in log:
                return False  # In der ersten Nacht keine Vorkenntnisse
        return True
