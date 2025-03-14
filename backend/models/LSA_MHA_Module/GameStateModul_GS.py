import random
import logging


class GameState:
    """
    Represents the current state of the game, including players and their roles.
    """

    def __init__(self, logger=None):
        self.players = {}
        self.global_conversation_log = []
        self.night_log = []  # Stores conversations during the night phase
        self.day_log = []    # Stores conversations during the day phase
        self.logger = logger or logging.getLogger(__name__)

    def initialize_roles(self, player_ids, strategies, human_player="Human"):
        """
        Initializes the roles of the players in the game.
        """
        roles = ['villager', 'villager', 'seer', 'werewolf', 'werewolf']
        random.shuffle(roles)

        for player_id, role in zip(player_ids, roles):
            self.players[player_id] = {
                "role": role,
                "awake": False,
                "remaining": True,
                "remaining_players": [p for p in player_ids + [human_player] if p != player_id],
                "conversation_log": [],
                "base_strategy": strategies.get(role, "Default strategy."),
                "last_statement": None
            }

        self.players[human_player] = {
            "role": "villager",
            "awake": False,
            "remaining": True,
            "remaining_players": [p for p in player_ids if p != human_player],
            "conversation_log": [],
            "base_strategy": "Analyze discussions and cast votes strategically.",
            "last_statement": None
        }

    def activate_player(self, player_id):
        """
        Activates a player, marking them as awake.
        """
        if player_id in self.players:
            self.players[player_id]['awake'] = True

    def deactivate_player(self, player_id):
        """
        Deactivates a player, marking them as not awake.
        """
        if player_id in self.players:
            self.players[player_id]['awake'] = False

    def get_remaining_players(self):
        """
        Returns a list of players who are still in the game.
        """
        return [player_id for player_id, state in self.players.items() if state['remaining']]

    def get_valid_targets(self, current_player):
        """
        Returns a list of valid targets for elimination based on the player's role.
        """
        current_role = self.get_role(current_player)
        return [
            player_id for player_id, state in self.players.items()
            if state['remaining'] and player_id != current_player
            and not (current_role == "werewolf" and state['role'] == "werewolf")
        ]

    def get_role(self, player_id):
        """
        Returns the role of the specified player.
        """
        return self.players.get(player_id, {}).get('role')

    def get_conversation_log(self, player_id):
        """
        Returns the local conversation log for a specific player.

        Args:
            player_id (str): The ID of the player whose conversation log is requested.

        Returns:
            list: A list of statements in the player's local conversation log.
        """
        if player_id in self.players:
            return self.players[player_id].get('conversation_log', [])
        else:
            self.logger.warning(f"Player {player_id} not found in game state.")
            return []  # Return an empty list if the player_id is invalid

    def get_players_with_role(self, role):
        """
        Returns a list of player IDs with the specified role who are still in the game.

        Args:
            role (str): The role to search for (e.g., 'werewolf').

        Returns:
            list: A list of player IDs with the specified role.
        """
        return [
            player_id for player_id, state in self.players.items()
            if state['role'] == role and state['remaining']
        ]

    def get_last_statement(self, player_id):
        """
        Returns the last statement made by a specific player.
        """
        return self.players.get(player_id, {}).get('last_statement')

    def add_to_conversation_log(self, speaker, statement, phase="day"):
        """
        Adds a statement to the global conversation log and updates player-specific logs
        for players who are awake.

         Args:
        speaker (str): The player making the statement.
        statement (str): The statement to log.
        phase (str): The current phase ("day" or "night").
        """
        # Skip if the speaker is not awake or if the speaker is eliminated
        if not self.players.get(speaker, {}).get("awake", False) or not self.players[speaker]["remaining"]:
            self.logger.warning(f"Skipping log entry for inactive player: {speaker}")
            return

        # Add to global log
        self.global_conversation_log.append((speaker, statement))
        self.logger.info(f"Global Log Update: {speaker}: {statement}")

        # Add to phase-specific logs
        if phase == "night" and self.players[speaker]["role"] == "werewolf":
            self.night_log.append((speaker, statement))
        elif phase == "day":
            self.day_log.append((speaker, statement))

        # Update individual player logs for awake players
        for player_id, state in self.players.items():
            if state["awake"]:  # Only awake players receive updates
                if phase == "night" and state["role"] != "werewolf":
                    continue  # Non-werewolves don't see night discussions
                state["conversation_log"].append((speaker, statement))
                if speaker == player_id:
                    state["last_statement"] = statement
        self.logger.info(f"Log updated for phase {phase}: {speaker} - {statement}")

    def display_game_state(self, exclude_global_log=False):
        """
        Displays the current game state for debugging.
        """
        print("\n--- Current Game State ---")
        for player_id, state in self.players.items():
            print(f"Player {player_id}: {state}")
        if not exclude_global_log:
            print(f"Global Conversation Log: {self.global_conversation_log}")
        print("--- End of Game State ---\n")

    def finalize_elimination(self, player_id):
        """
        Marks a player as eliminated and updates the game state.

        Args:
            player_id (str): The ID of the player to eliminate.
        """
        if player_id not in self.players:
            self.logger.warning(f"Player {player_id} not found in game state.")  # #UPDATE!!!
            return "Unknown role"

        # Get the player's role
        role = self.players[player_id]["role"]

        # Mark the player as eliminated
        self.players[player_id]['remaining'] = False
        self.players[player_id]['awake'] = False

        #Remove the eliminated player from all remaining_players lists
        for state in self.players.values():
            if player_id in state["remaining_players"]:
                state["remaining_players"].remove(player_id)

        # Log elimination
        if player_id == "Human":
            print("You have been eliminated. You are now a spectator.")
        else:
            print(f"Player {player_id} ({role}) has been eliminated.")

        return role

    def to_dict(self):
        """
        Converts the game state to a dictionary format.
        """
        return {
            "players": self.players,
            "global_conversation_log": self.global_conversation_log
        }