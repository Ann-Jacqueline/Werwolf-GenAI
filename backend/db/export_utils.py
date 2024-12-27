import json
from backend.db.db_utils import connect_to_db

json_output_path = r'C:\Users\PC\Desktop\WerwolfIQ\Werwolf-GenAI\backend\output.json'

def export_to_json(json_output_path):
    """
    Export all game data to a JSON file with players grouped under their respective games.
    """
    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch all games
    cursor.execute('''
    SELECT game_id, title, started_at, ended_at, winner_role
    FROM Game
    ''')
    games = cursor.fetchall()

    # Fetch players per game
    cursor.execute('''
    SELECT game_id, player_name, player_role, eliminated_at_phase, is_human
    FROM Player
    ''')
    players = cursor.fetchall()

    # Fetch phases and responses
    cursor.execute('''
    SELECT 
        ph.game_id, ph.phase_name, ph.eliminated_player_id,
        pr.player_id, pr.prompt, pr.response, pr.created_at, pl.player_name AS responding_player_name
    FROM Phase ph
    LEFT JOIN Prompt_Responses pr ON ph.phase_id = pr.phase_id
    LEFT JOIN Player pl ON pr.player_id = pl.player_id
    ''')
    phases_responses = cursor.fetchall()

    # Organize data hierarchically
    data = []
    for game in games:
        game_id = game[0]
        game_data = {
            "game_id": game_id,
            "title": game[1],
            "started_at": game[2],
            "ended_at": game[3],
            "winner_role": game[4],
            "players": [
                {
                    "player_name": p[1],
                    "player_role": p[2],
                    "eliminated_at_phase": p[3],
                    "is_human": p[4]
                } for p in players if p[0] == game_id
            ],
            "phases": [
                {
                    "phase_name": pr[1],
                    "eliminated_player_id": pr[2],
                    "responses": [
                        {
                            "player_id": pr[3],
                            "player_name": pr[7],
                            "prompt": pr[4],
                            "response": pr[5],
                            "created_at": pr[6]
                        }
                    ]
                } for pr in phases_responses if pr[0] == game_id
            ]
        }
        data.append(game_data)

    # Write to JSON file
    with open(json_output_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"DEBUG: Data successfully exported to {json_output_path}.")
    conn.close()
