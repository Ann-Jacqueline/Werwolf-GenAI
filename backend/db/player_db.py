from backend.db.db_utils import connect_to_db

def add_player(game_id, player_name, player_role=None, is_human=False):
    """
    Adds a single player to the Player table.

    Args:
        game_id (int): The ID of the game the player is part of.
        player_name (str): The name of the player.
        player_role (str, optional): The role assigned to the player. Defaults to None.
        is_human (bool): Whether the player is human. Defaults to False.

    Returns:
        int: The ID of the newly added player.
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Player (game_id, player_name, player_role, is_human)
    VALUES (?, ?, ?, ?)
    ''', (game_id, player_name, player_role, is_human))
    conn.commit()
    player_id = cursor.lastrowid
    conn.close()
    return player_id

def get_players(game_id):
    """
    Retrieves all players for a specific game.

    Args:
        game_id (int): The ID of the game.

    Returns:
        list[dict]: A list of dictionaries, each representing a player.
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT player_id, player_name, player_role, is_human FROM Player WHERE game_id = ?", (game_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "player_id": row[0],
            "player_name": row[1],
            "player_role": row[2],
            "is_human": row[3],
        }
        for row in rows
    ]

def update_player_role(player_id, player_role):
    """
    Updates the role of a specific player.

    Args:
        player_id (int): The ID of the player.
        player_role (str): The role to assign to the player.
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Player SET player_role = ? WHERE player_id = ?", (player_role, player_id))
    conn.commit()
    conn.close()

def eliminate_player(player_id, phase_id):
    """
    Marks a player as eliminated by setting their eliminated_at_phase.

    Args:
        player_id (int): The ID of the player to eliminate.
        phase_id (int): The ID of the phase in which the player was eliminated.
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Player SET eliminated_at_phase = ? WHERE player_id = ?", (phase_id, player_id))
    conn.commit()
    conn.close()

def get_human_players(game_id):
    """
    Retrieves all human players for a specific game.

    Args:
        game_id (int): The ID of the game.

    Returns:
        list[dict]: A list of dictionaries, each representing a human player.
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT player_id, player_name FROM Player WHERE game_id = ? AND is_human = 1", (game_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "player_id": row[0],
            "player_name": row[1],
        }
        for row in rows
    ]

def get_ai_players(game_id):
    """
    Retrieves all AI players for a specific game.

    Args:
        game_id (int): The ID of the game.

    Returns:
        list[dict]: A list of dictionaries, each representing an AI player.
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT player_id, player_name FROM Player WHERE game_id = ? AND is_human = 0", (game_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "player_id": row[0],
            "player_name": row[1],
        }
        for row in rows
    ]
