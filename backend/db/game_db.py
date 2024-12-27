from backend.db.db_utils import connect_to_db

def start_game(total_players):
    """
    Starts a new game and saves the total number of players.

    Args:
        total_players (int): The total number of players in the game (human + AI).

    Returns:
        int: The ID of the newly created game.
    """
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Insert the game details with the total number of players
        cursor.execute('''
        INSERT INTO Game (title, num_players)
        VALUES (?, ?)
        ''', ("Placeholder", total_players))
        conn.commit()

        # Return the newly created game ID
        game_id = cursor.lastrowid

        title = f"Werewolf Game {game_id}"
        cursor.execute('''
        UPDATE Game
        SET title = ?
        WHERE game_id = ?
        ''', (title, game_id))
        conn.commit()

        return game_id

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

def end_game(game_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Game SET ended_at = CURRENT_TIMESTAMP WHERE game_id = ?", (game_id,))
    conn.commit()
    conn.close()
