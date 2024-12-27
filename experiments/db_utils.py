import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'prompts.db')

def initialize_database():
    print(f"DEBUG: Initialisiere Datenbank unter {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabelle `game_rounds`
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_rounds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ended_at TIMESTAMP DEFAULT NULL
    )
    ''')

    # Tabelle `prompts_responses`
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prompts_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_round_id INTEGER,
        round_number INTEGER,
        prompt TEXT,
        response TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (game_round_id) REFERENCES game_rounds(id)
    )
    ''')

    conn.commit()
    conn.close()
    print("DEBUG: Datenbank erfolgreich initialisiert.")

def save_to_database(prompt, response, game_round_id, round_number):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Prompt und Response hinzufügen
        cursor.execute('''
        INSERT INTO prompts_responses (game_round_id, round_number, prompt, response)
        VALUES (?, ?, ?, ?)
        ''', (game_round_id, round_number, prompt, response))

        conn.commit()
        print(f"DEBUG: Prompt und Response erfolgreich gespeichert für Spielrunde {game_round_id}, Runde {round_number}.")
    except sqlite3.Error as e:
        print(f"Fehler beim Speichern in der Datenbank: {e}")
    finally:
        conn.close()

def export_to_json(db_path, json_output_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Daten aus den Tabellen abrufen (mit JOIN)
    cursor.execute('''
    SELECT 
        g.id AS game_round_id,
        g.title AS game_round_title,
        g.started_at,
        g.ended_at,
        p.round_number,
        p.prompt,
        p.response,
        p.created_at AS response_created_at
    FROM game_rounds g
    LEFT JOIN prompts_responses p ON g.id = p.game_round_id
    ORDER BY g.id, p.round_number
    ''')
    rows = cursor.fetchall()

    # Spaltennamen für JSON-Keys abrufen
    columns = [description[0] for description in cursor.description]

    # Daten in JSON-konformes Format umwandeln
    data = [dict(zip(columns, row)) for row in rows]

    # JSON-Datei speichern
    with open(json_output_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"DEBUG: Daten erfolgreich in {json_output_path} exportiert.")
    conn.close()

if __name__ == '__main__':
    initialize_database()  # Datenbank initialisieren
    save_to_database("Wie spielt man Werwolf?", "Antwort: [...]", 3, 5)
    save_to_database("Wer ist der Werwolf?", "Antwort: Spielerin A", 3, 6)
    export_to_json(DB_PATH, '../backend/output.json')

