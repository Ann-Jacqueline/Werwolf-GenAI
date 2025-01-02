import random


class GameState:
    """
    Represents the current state of the game, including players and their roles.
    """

    def __init__(self):
        self.players = {}  # Player states (player_id -> state dict)
        self.global_conversation_log = []  # Global log of discussions

    def initialize_roles(self, player_ids, strategies, human_player="Human"):
        roles = ['villager', 'villager', 'seer', 'werewolf', 'werewolf']
        random.shuffle(roles)

        for player_id, role in zip(player_ids, roles):
            self.players[player_id] = {
                "role": role,
                "awake": False,
                "remaining": True,
                "remaining_players": player_ids[:],
                "conversation_log": [],
                "base_strategy": strategies.get(role, "Default strategy."),
                "last_statement": None
            }

        self.players[human_player] = {
            "role": "villager",
            "awake": False,
            "remaining": True,
            "remaining_players": player_ids[:],
            "conversation_log": [],
            "base_strategy": "Analyze discussions and cast votes strategically.",
            "last_statement": None
        }

        print("Roles initialized:")
        for player_id, state in self.players.items():
            print(f"Player {player_id}: {state['role']} with strategy: {state['base_strategy']}")

    def get_role(self, player_id):
        if player_id in self.players:
            return self.players[player_id]['role']
        return None

    def get_remaining_players(self):
        return [
            player_id for player_id, state in self.players.items()
            if state['remaining']
        ]

    def get_valid_targets(self, current_player):
        current_role = self.get_role(current_player)
        if current_role is None:
            raise ValueError(f"Invalid player ID: {current_player}")

        return [
            player_id for player_id, state in self.players.items()
            if state['remaining'] and player_id != current_player and (
                    current_role != "werewolf" or state['role'] != "werewolf"
            )
        ]

    def activate_player(self, player_id):
        if player_id in self.players:
            self.players[player_id]['awake'] = True

    def deactivate_player(self, player_id):
        if player_id in self.players:
            self.players[player_id]['awake'] = False

    def get_players_with_role(self, role):
        return [player_id for player_id, state in self.players.items()
                if state['role'] == role and state['remaining']]

    def finalize_elimination(self, player_id):
        if player_id in self.players:
            self.players[player_id]['remaining'] = False
            self.players[player_id]['awake'] = False
            for state in self.players.values():
                if player_id in state['remaining_players']:
                    state['remaining_players'].remove(player_id)
            print(f"Player {player_id} has been eliminated.")

    def get_conversation_log(self):
        return self.global_conversation_log

    def add_to_conversation_log(self, player_id, statement):
        if player_id in self.players:
            self.players[player_id]['conversation_log'].append(statement)
            self.players[player_id]['last_statement'] = statement
            self.global_conversation_log.append((player_id, statement))

    def get_last_statement(self, player_id):
        """
        Returns the last statement made by a specific player.
        """
        if player_id in self.players:
            return self.players[player_id].get('last_statement', None)
        return None

    def calculate_intermediate_votes(self):
        vote_counts = {}
        for _, statement in self.global_conversation_log:
            if "target Player" in statement:
                target = statement.split("target Player")[-1].strip()
                vote_counts[target] = vote_counts.get(target, 0) + 1
        return vote_counts

    def to_dict(self):
        return {
            "players": self.players,
            "global_conversation_log": self.global_conversation_log
        }
