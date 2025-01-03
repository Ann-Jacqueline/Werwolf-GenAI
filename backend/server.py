from flask import Flask, jsonify, request
from flask_cors import CORS
from db.schema import initialize_database
from db.game_db import start_game, end_game
from db.prompt_db import save_prompt_response
from db.export_utils import export_to_json
from models.LSA_MHA_Module.GlobalHistoryModul_GH import GlobalHistoryModel

import os




app = Flask(__name__)
CORS(app)

# API Status Check
@app.route("/api", methods=['GET'])
def api_status():
    return jsonify({"status": "Backend is running successfully!"})

@app.route("/api/data", methods=['GET'])
def api_data():
    return jsonify({"message": "Backend is running."})

@app.route("/api/start_game", methods=['POST'])
def start_game_route():
    data = request.json
    human_players = data.get("human_players", 1)
    total_players = data.get("total_players", 7)  # Default to 7 if not provided

    if not 1 <= human_players <= total_players:
        return jsonify({"error": "Invalid player counts."}), 400

    try:
        # Start a new game and store the number of total players
        game_id = start_game(total_players)  # Pass total_players to start_game
        return jsonify({"message": "Game started", "game_id": game_id}), 200
    except Exception as e:
        return jsonify({"error": f"Error starting game: {str(e)}"}), 500


@app.route("/api/end_game", methods=['POST'])
def end_game_route():
    data = request.json
    game_id = data.get("game_id")

    if not game_id:
        return jsonify({"error": "game_id is required."}), 400

    try:
        # End the game
        end_game(game_id)
        return jsonify({"message": f"Game {game_id} ended successfully."}), 200

    except Exception as e:
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
        relevant_log = global_history.get_recent_announcements(limit=1)
        return jsonify({
            "relevant_log": relevant_log[0] if relevant_log else "No relevant logs yet."
        }), 200
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
