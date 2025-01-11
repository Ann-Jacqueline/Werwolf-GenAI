class GameState:
    """
    Die GameState-Klasse repräsentiert den Zustand eines einzelnen Spielers im Spiel.
    """
    def __init__(self):
        """
        Initialisiert den Spielzustand mit Standardwerten.
        """
        self.role = None  # Rolle des Spielers (e.g., villager, werewolf, seer)
        self.awake = False  # Ob der Spieler aktiv (wach) ist
        self.remaining_players = []  # Liste der verbleibenden Spieler
        self.conversation_log = []  # Protokoll der Diskussionen und Aussagen
        self.last_statement = None  # Die letzte Aussage des Spielers
        self.base_strategy = None  # Basisstrategie, abhängig von der Rolle

    def set_awake(self, status):
        """
        Updates the 'awake' status of the player.

        Args:
            status (bool): True if the player is active, False otherwise.
        """
        self.awake = status

    def update_role_and_strategy(self, role):
        """
        Aktualisiert die Rolle des Spielers und setzt die entsprechende Strategie.
        """
        self.role = role
        strategies = {
            "villager": "Focus on gathering information and identifying suspicious behavior and focus on identifying and eliminating the werwolfs.",
            "werewolf": "Deflect suspicion, manipulate discussions, and work with your ally to eliminate threats.",
            "seer": "Provide subtle hints about suspicions without revealing your role prematurely. Also try identity who could be a potential werwolf and aid to eliminate them"
        }
        self.base_strategy = strategies.get(role, "Play according to the current game context.")

    def add_to_conversation_log(self, speaker, statement):
        """
        Fügt einen Eintrag zum Gesprächsprotokoll hinzu.

        Args:
            speaker (str): Der Spieler, der die Aussage gemacht hat.
            statement (str): Die Aussage selbst.
        """
        if not self.conversation_log or self.conversation_log[-1] != (speaker, statement):
            self.conversation_log.append((speaker, statement))
            self.last_statement = statement

    def to_dict(self):
        return {
            "role": self.role,
            "awake": self.awake,
            "remaining_players": self.remaining_players,
            "conversation_log": self.conversation_log,
            "base_strategy": self.base_strategy,
            "last_statement": self.last_statement
        }

    def track_vote(self, voter, target):
        """
        Tracks a vote for elimination.

        Args:
            voter (str): The player who is voting.
            target (str): The target player being voted for elimination.
        """
        vote_statement = f"{voter} votes to eliminate Player {target}"
        self.add_to_conversation_log(voter, vote_statement)

    def track_agreement(self, supporter, target):
        """
        Tracks an explicit agreement with targeting a player.

        Args:
            supporter (str): The player who is supporting.
            target (str): The target player being supported.
        """
        agreement_statement = f"{supporter} agrees with targeting Player {target}"
        self.add_to_conversation_log(supporter, agreement_statement)

    def remove_player(self, player):
        """
        Entfernt einen Spieler aus der Liste der verbleibenden Spieler.

        Args:
            player (str): Der zu entfernende Spieler.
        """
        if player in self.remaining_players:
            self.remaining_players.remove(player)
