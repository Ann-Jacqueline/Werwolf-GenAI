from flask import Flask, jsonify, request
from flask_cors import CORS
from db.schema import initialize_database
from db.game_db import start_game, end_game
from db.prompt_db import save_prompt_response
from db.export_utils import export_to_json
from models.LSA_MHA_Module.Orchestrator import Orchestrator
import threading

import os
print(f"Current working directory: {os.getcwd()}")

app = Flask(__name__)
CORS(app)

# API Status Check
@app.route("/api", methods=['GET'])
def api_status():
    return jsonify({"status": "Backend is running successfully!"})

@app.route("/api/data", methods=['GET'])
def api_data():
    return jsonify({"message": "Backend is running."})

active_game_id = None
orchestrator = Orchestrator()

@app.route("/api/start_game", methods=['POST'])
def start_game_route():
    global active_game_id, orchestrator_thread
    print(f"Before starting game: active_game_id={active_game_id}")  # Debug

    if active_game_id is not None:
        print(f"Game already running with ID {active_game_id}.")  # Debug
        return jsonify({"error": "Already running!", "game_id": active_game_id}), 400

    try:
        data = request.json
        total_players = data.get("total_players", 7)
        game_id = start_game(total_players)
        active_game_id = game_id
        orchestrator_thread = threading.Thread(target=orchestrator.start_game(), daemon=True)
        orchestrator_thread.start()
        print(f"New game started with ID: {active_game_id}")  # Debug
        return jsonify({"message": "Game started", "game_id": active_game_id}), 200
    except Exception as e:
        print(f"Error starting game: {e}")  # Debug
        return jsonify({"error": f"Error starting game: {str(e)}"}), 500

@app.route("/api/next_phase", methods=['POST'])
def next_phase():
    global orchestrator
    try:
        orchestrator.handle_phase()  # Nur eine Phase ausführen
        return jsonify({"message": "Phase handled", "current_phase": orchestrator.phase}), 200
    except Exception as e:
        return jsonify({"error": f"Error handling phase: {str(e)}"}), 500

@app.route("/api/end_game", methods=['POST'])
def end_game_route():
    global active_game_id
    print(f"Before ending game: active_game_id={active_game_id}")  # Debug

    if active_game_id is None:
        print("No active game to end.")  # Debug
        return jsonify({"error": "No active game"}), 400

    data = request.json
    game_id = data.get("game_id")

    if game_id != active_game_id:
        print(f"Invalid game_id. Expected {active_game_id}, got {game_id}.")  # Debug
        return jsonify({"error": "Invalid game_id."}), 400

    try:
        end_game(game_id)
        active_game_id = None
        print("Game ended successfully.")  # Debug
        return jsonify({"message": f"Game {game_id} ended successfully."}), 200
    except Exception as e:
        print(f"Error ending game: {e}")  # Debug
        return jsonify({"error": f"Error ending game: {str(e)}"}), 500


@app.route("/api/data", methods=['POST'])
def process_prompt():
    data = request.json
    prompt = data.get("prompt", '')
    response = data.get("response", '')
    game_id = data.get("game_id")
    phase_id = data.get("phase_id")
    player_id = data.get("player_id")  # Use None for moderator responses

    if not game_id or not phase_id:
        return jsonify({"error": "game_id and phase_id are required."}), 400

    try:
        # Save prompt and response
        save_prompt_response(game_id, phase_id, player_id, prompt, response)
        return jsonify({"message": "Prompt and response saved successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"Error processing prompt: {str(e)}"}), 500


@app.route("/api/log", methods=["GET"])
def fetch_log():
    try:
        log_file_path = os.path.join(os.path.dirname(__file__), "models", "LSA_MHA_Module", "game_log.txt")

        # Lese die letzten 10 Zeilen aus der Log-Datei
        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as log_file:
                logs = log_file.readlines()[-10:]  # Letzten 10 Zeilen lesen
        else:
            logs = ["Log file not found."]

        # Rückgabe der Logs als JSON
        return jsonify({"console_output": logs}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to fetch logs: {str(e)}"}), 500



@app.route("/api/export", methods=['GET'])
def export_data():
    try:
        # Define the path for output.json inside the backend package
        output_path = os.path.join(os.path.dirname(__file__), 'output.json')
        export_to_json(output_path)
        return jsonify({"message": f"Data exported to {output_path}"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to export data: {str(e)}"}), 500


if __name__ == "__main__":
    initialize_database()  # Ensure tables exist
    app.run(debug=True)
