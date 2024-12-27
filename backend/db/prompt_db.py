from backend.db.db_utils import connect_to_db

def save_prompt_response(game_id, phase_id, player_id, prompt, response):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Prompt_Responses (game_id, phase_id, player_id, prompt, response)
    VALUES (?, ?, ?, ?, ?)
    ''', (game_id, phase_id, player_id, prompt, response))
    conn.commit()
    conn.close()