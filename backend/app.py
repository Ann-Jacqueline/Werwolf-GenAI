from flask import Flask, jsonify, request
from flask_cors import CORS
from db_utils import save_to_database, DB_PATH
import sqlite3
import os
from transformers import pipeline
from token_tracker import TokenTracker


DB_PATH = './backend/prompts.db'

app = Flask(__name__)
CORS(app)

'''
tracker = TokenTracker(model_name="meta-llama/Llama-2-13b-chat-hf")
API_KEY = os.getenv('HUGGING_FACE_API_KEY')

def get_llama_response(prompt):
    model_name = "meta-llama/Llama-2-13b-chat-hf"
    generator = pipeline('text-generation', model=model_name, use_auth_token=API_KEY
                         )
    response = generator(prompt, max_length= 150,num_return_sequences=1)
    return response[0]['generated_text']
'''

# API läuft
@app.route("/api", methods=['GET'])
def api_status():
    return jsonify({"status": "Backend laeuft erfolgreich!"})


@app.route("/api/data", methods=['GET'])
def api_data():
    example_data = {"message": "BE laeuft."}
    return jsonify(example_data)


@app.route("/api/data", methods=['POST'])
def process_prompt():
    data = request.json
    prompt = data.get("prompt", '')
    response = data.get("response", '')
    game_round_id = data.get("game_round_id")
    round_number = data.get("round_number")
    print(f"DEBUG: Eingabewerte: prompt={prompt}, respone = {response}, game_round_id={game_round_id}, round_number={round_number}")

    # Validierung der Eingabewerte
    if not isinstance(game_round_id, int):
        return jsonify({"error": "game_round_id muss ein Integer sein"}), 400
    if not isinstance(round_number, int):
        return jsonify({"error": "round_number muss ein Integer sein"}), 400
    if not isinstance(prompt, str) or not isinstance(response, str):
        return jsonify({"error": "prompt und response müssen Strings sein"}), 400

    try:
        response = f"Dummy Antwort: {prompt}"
    except Exception as e:
        return jsonify({ "error": f"Fehler beim Abrufen der Antwort: {str(e)}"}),500

    input_tokens, output_tokens, total_tokens = 0,0,0

   # if tracker.is_limit_reached():
   #     return jsonify({"error": "Limit ist erreicht.", "usage" : tracker.get_usage()}), 403

    save_to_database(prompt, response, game_round_id, round_number)

    return jsonify({
        "prompt": prompt,
        "response": response,
        "game_round_id": game_round_id,
        "round_number": round_number
    }), 200

@app.route("/api/start_game", methods=['POST'])
def start_game():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT MAX(id) FROM game_rounds')
        last_game_id = cursor.fetchone()[0]

        new_game_id = (last_game_id or 0) + 1
        cursor.execute('''
        INSERT INTO game_rounds (id, title)
        VALUES (?, ?)
        ''', (new_game_id, f"Spielrunde {new_game_id}"))

        conn.commit()
        print(f"DEBUG: Neue Spielrunde gestartet, ID={new_game_id}")
        return jsonify({"message": "Spiel gestartet", "game_round_id": new_game_id}), 200
    except sqlite3.Error as e:
        print(f"Fehler beim Starten der Spielrunde: {e}")
        conn.rollback()
        return jsonify({"error": "Fehler beim Starten der Spielrunde"}), 500
    finally:
        conn.close()

@app.route("/api/end_game", methods=['POST'])
def end_game():
    data = request.json
    game_round_id = data.get("game_round_id")

    if not game_round_id:
        return jsonify({"error": "game_round_id wird benötigt"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Prüfe, ob die Spielrunde existiert
        cursor.execute('SELECT id FROM game_rounds WHERE id = ?', (game_round_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": f"Spielrunde {game_round_id} existiert nicht"}), 404

        # Aktualisiere die Spalte `ended_at` mit dem aktuellen Zeitstempel
        cursor.execute('''
        UPDATE game_rounds
        SET ended_at = CURRENT_TIMESTAMPfrom flask import Flask, jsonify, request
from flask_cors import CORS
from db_utils import save_to_database, DB_PATH
import sqlite3
import os
from transformers import pipeline
from token_tracker import TokenTracker


DB_PATH = './backend/prompts.db'

app = Flask(__name__)
CORS(app)

'''
tracker = TokenTracker(model_name="meta-llama/Llama-2-13b-chat-hf")
API_KEY = os.getenv('HUGGING_FACE_API_KEY')

def get_llama_response(prompt):
    model_name = "meta-llama/Llama-2-13b-chat-hf"
    generator = pipeline('text-generation', model=model_name, use_auth_token=API_KEY
                         )
    response = generator(prompt, max_length= 150,num_return_sequences=1)
    return response[0]['generated_text']
'''

# API läuft
@app.route("/api", methods=['GET'])
def api_status():
    return jsonify({"status": "Backend laeuft erfolgreich!"})


@app.route("/api/data", methods=['GET'])
def api_data():
    example_data = {"message": "BE laeuft."}
    return jsonify(example_data)


@app.route("/api/data", methods=['POST'])
def process_prompt():
    data = request.json
    prompt = data.get("prompt", '')
    response = data.get("response", '')
    game_round_id = data.get("game_round_id")
    round_number = data.get("round_number")
    print(f"DEBUG: Eingabewerte: prompt={prompt}, respone = {response}, game_round_id={game_round_id}, round_number={round_number}")

    # Validierung der Eingabewerte
    if not isinstance(game_round_id, int):
        return jsonify({"error": "game_round_id muss ein Integer sein"}), 400
    if not isinstance(round_number, int):
        return jsonify({"error": "round_number muss ein Integer sein"}), 400
    if not isinstance(prompt, str) or not isinstance(response, str):
        return jsonify({"error": "prompt und response müssen Strings sein"}), 400

    try:
        response = f"Dummy Antwort: {prompt}"
    except Exception as e:
        return jsonify({ "error": f"Fehler beim Abrufen der Antwort: {str(e)}"}),500

    input_tokens, output_tokens, total_tokens = 0,0,0

   # if tracker.is_limit_reached():
   #     return jsonify({"error": "Limit ist erreicht.", "usage" : tracker.get_usage()}), 403

    save_to_database(prompt, response, game_round_id, round_number)

    return jsonify({
        "prompt": prompt,
        "response": response,
        "game_round_id": game_round_id,
        "round_number": round_number
    }), 200

@app.route("/api/start_game", methods=['POST'])
def start_game():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT MAX(id) FROM game_rounds')
        last_game_id = cursor.fetchone()[0]

        new_game_id = (last_game_id or 0) + 1
        cursor.execute('''
        INSERT INTO game_rounds (id, title)
        VALUES (?, ?)
        ''', (new_game_id, f"Spielrunde {new_game_id}"))

        conn.commit()
        print(f"DEBUG: Neue Spielrunde gestartet, ID={new_game_id}")
        return jsonify({"message": "Spiel gestartet", "game_round_id": new_game_id}), 200
    except sqlite3.Error as e:
        print(f"Fehler beim Starten der Spielrunde: {e}")
        conn.rollback()
        return jsonify({"error": "Fehler beim Starten der Spielrunde"}), 500
    finally:
        conn.close()

@app.route("/api/end_game", methods=['POST'])
def end_game():
    data = request.json
    game_round_id = data.get("game_round_id")

    if not game_round_id:
        return jsonify({"error": "game_round_id wird benötigt"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Prüfe, ob die Spielrunde existiert
        cursor.execute('SELECT id FROM game_rounds WHERE id = ?', (game_round_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": f"Spielrunde {game_round_id} existiert nicht"}), 404

        # Aktualisiere die Spalte `ended_at` mit dem aktuellen Zeitstempel
        cursor.execute('''
        UPDATE game_rounds
        SET ended_at = CURRENT_TIMESTAMP
        WHERE id = ?
        ''', (game_round_id,))
        conn.commit()

        print(f"DEBUG: Spielrunde {game_round_id} beendet.")
        return jsonify({"message": f"Spielrunde {game_round_id} beendet"}), 200
    except sqlite3.Error as e:
        print(f"Fehler beim Beenden der Spielrunde: {e}")
        conn.rollback()
        return jsonify({"error": "Fehler beim Beenden der Spielrunde"}), 500
    finally:
        conn.close()




if __name__ == "__main__":
    app.run(debug=True)

        WHERE id = ?
        ''', (game_round_id,))
        conn.commit()

        print(f"DEBUG: Spielrunde {game_round_id} beendet.")
        return jsonify({"message": f"Spielrunde {game_round_id} beendet"}), 200
    except sqlite3.Error as e:
        print(f"Fehler beim Beenden der Spielrunde: {e}")
        conn.rollback()
        return jsonify({"error": "Fehler beim Beenden der Spielrunde"}), 500
    finally:
        conn.close()




if __name__ == "__main__":
    app.run(debug=True)
