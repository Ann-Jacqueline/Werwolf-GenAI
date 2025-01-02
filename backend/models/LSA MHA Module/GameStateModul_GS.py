import random


class GameState:
    """
    Represents the current state of the game, including players and their roles.
    """

    def __init__(self):
        self.players = {}  # Player states (player_id -> state dict)
        self.global_conversation_log = []  # Global log of discussions

    def initialize_roles(self, player_ids, strategies, human_player="Human"):
        """
        Initializes roles for all players, including the human player.
        """
        roles = ['villager', 'villager', 'seer', 'werewolf', 'werewolf']
        random.shuffle(roles)

        for player_id, role in zip(player_ids, roles):
            self.players[player_id] = {
                "role": role,
                "awake": True,
                "remaining_players": player_ids[:],
                "conversation_log": [],
                "base_strategy": strategies.get(role, "Play according to the current game context."),
                "last_statement": None
            }

        self.players[human_player] = {
            "role": "villager",  # Example role
            "awake": True,
            "remaining_players": player_ids[:],
            "conversation_log": [],
            "base_strategy": "Analyze discussions and cast votes strategically.",
            "last_statement": None
        }

        print("Roles initialized:")
        for player_id, state in self.players.items():
            print(f"Player {player_id}: {state['role']} with strategy: {state['base_strategy']}")

    def get_remaining_players(self):
        """
        Returns a list of players who are still active (not eliminated).
        """
        return [
            player_id for player_id, state in self.players.items()
            if state['awake']
        ]

    def add_to_conversation_log(self, player_id, statement):
        """
        Adds a statement to the player's and global conversation logs.
        """
        if player_id in self.players:
            self.players[player_id]['conversation_log'].append(statement)
            self.players[player_id]['last_statement'] = statement
            self.global_conversation_log.append((player_id, statement))

    def calculate_intermediate_votes(self):
        """
        Calculates the vote tallies based on the global conversation log.

        Returns:
            dict: A dictionary with player IDs as keys and vote counts as values.
        """
        vote_counts = {}
        for _, statement in self.global_conversation_log:
            if "target Player" in statement:
                target = statement.split("target Player")[-1].strip()
                vote_counts[target] = vote_counts.get(target, 0) + 1
        return vote_counts

    def get_last_statement(self, player_id):
        """
        Returns the last statement made by the specified player.
        """
        if player_id in self.players:
            return self.players[player_id]['last_statement']
        return None

    def get_valid_targets(self, current_player):
        """
        Returns a list of valid targets for elimination, excluding the current player's teammates if applicable.
        """
        current_role = self.get_role(current_player)
        return [
            player_id for player_id, state in self.players.items()
            if state['awake'] and player_id != current_player and (
                    current_role != "werewolf" or self.get_role(player_id) != "werewolf"
            )
        ]

    def finalize_elimination(self, player_id):
        """
        Marks a player as eliminated and updates the game state.
        """
        if player_id in self.players:
            self.players[player_id]['awake'] = False
            self.remove_player(player_id)
            print(f"Player {player_id} has been eliminated.")

    def get_last_eliminated_player(self):
        """
        Returns the most recently eliminated player based on the global log.
        """
        for player, statement in reversed(self.global_conversation_log):
            if "has been eliminated" in statement:
                return player
        return None

    def remove_player(self, player_id):
        """
        Removes a player from the list of remaining players.
        """
        for state in self.players.values():
            if player_id in state['remaining_players']:
                state['remaining_players'].remove(player_id)

    def get_role(self, player_id):
        """
        Returns the role of the specified player.
        """
        return self.players.get(player_id, {}).get("role")

    def get_players_with_role(self, role):
        """
        Returns a list of players with the specified role who are still awake.
        """
        return [player_id for player_id, state in self.players.items() if state['role'] == role and state['awake']]

    def get_conversation_log(self):
        """
        Returns the global conversation log.
        """
        return self.global_conversation_log

    def to_dict(self):
        """
        Converts the game state to a dictionary format.
        """
        return {
            "players": self.players,
            "global_conversation_log": self.global_conversation_log
        }
