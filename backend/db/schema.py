from backend.db.db_utils import connect_to_db, DB_PATH

def initialize_database():
    """
    Initializes the database by creating all necessary tables.
    """
    print(f"DEBUG: Database path is {DB_PATH}")  # Log the database path
    conn = connect_to_db()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Game (
        game_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ended_at TIMESTAMP DEFAULT NULL,
        winner_role TEXT,
        num_players INTEGER  -- New column to store the number of players
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Player (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id INTEGER,
        player_name TEXT,
        player_role TEXT,
        eliminated_at_phase INTEGER,
        is_human BOOLEAN DEFAULT FALSE,  -- New column to indicate if the player is human
        FOREIGN KEY (game_id) REFERENCES Game(game_id),
        FOREIGN KEY (eliminated_at_phase) REFERENCES Phase(phase_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Phase (
        phase_id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id INTEGER,
        phase_name TEXT,
        eliminated_player_id INTEGER,
        FOREIGN KEY (game_id) REFERENCES Game(game_id),
        FOREIGN KEY (eliminated_player_id) REFERENCES Player(player_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Phase_Eliminations (
        elimination_id INTEGER PRIMARY KEY AUTOINCREMENT,
        phase_id INTEGER,
        eliminated_player_id INTEGER,
        FOREIGN KEY (phase_id) REFERENCES Phase(phase_id),
        FOREIGN KEY (eliminated_player_id) REFERENCES Player(player_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Prompt_Responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id INTEGER,
        phase_id INTEGER,
        player_id INTEGER,
        prompt TEXT,
        response TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (game_id) REFERENCES Game(game_id),
        FOREIGN KEY (phase_id) REFERENCES Phase(phase_id),
        FOREIGN KEY (player_id) REFERENCES Player(player_id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Database initialization completed.")
