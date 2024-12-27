from backend.db.db_utils import connect_to_db

def start_phase(game_id, phase_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Phase (game_id, phase_name) VALUES (?, ?)
    ''', (game_id, phase_name))
    conn.commit()
    phase_id = cursor.lastrowid
    conn.close()
    return phase_id
