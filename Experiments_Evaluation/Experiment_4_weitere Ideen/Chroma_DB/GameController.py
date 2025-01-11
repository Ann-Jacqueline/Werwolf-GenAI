# GameController.py
"""
Hauptsteuerung des Spiels.

Die GameController-Klasse verwaltet die Initialisierung, Speicherung und Verarbeitung von Spielzuständen,
Agenten und Ereignissen sowie die Spielphasen.
"""


import random
import os
import logging
import re
from uuid import uuid4
from openai import OpenAI
from chroma_client import (
    agents_collection,
    events_collection,
    game_state_collection
)


class GameController:
    """
        Verwaltet die Spielphasen und Interaktionen der Spieler.

        Attributes:
            logger (Logger): Logger zur Protokollierung von Spielereignissen.
            api_key (str): OpenAI-API-Schlüssel für GPT-basierte Entscheidungen.
            client (OpenAI): OpenAI-Client zur Interaktion mit GPT.
            persistent_game_state (dict): Der persistente Zustand des Spiels.
            phase (str): Die aktuelle Phase des Spiels ('night' oder 'day').
            round_number (int): Die aktuelle Rundennummer.
        """
    def __init__(self):
        # Configure logging
        logging.basicConfig(
            filename="game_log.txt",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

        # Load API key from environment variable
        self.api_key = os.getenv("YOUR_API_KEY")
        if not self.api_key:
            raise ValueError("Environment variable 'YOUR_API_KEY' is not set!")

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

        self.persistent_game_state = {
            'players': {},
            'history': {
                "phase": {"night": 0, "day": 0},
                "remaining_players": [],
                "last_statement": {},
                "conversation_log": [],
                "past_rounds": []
            }
        }

        self.phase = "night"
        self.round_number = 1

    # Agenten in ChromaDB speichern
    def register_agents(self):
        """
        Fügt vorab definierte Agenten zur Agenten-Sammlung hinzu.
        """
        agents = [
            {"role": "werewolf", "name": "Player D"},
            {"role": "seer", "name": "Player B"}
        ]
        agents_collection.add(
            documents=agents,
            ids=[str(uuid4()) for _ in agents]
        )

    # Spielzustände speichern
    def save_game_state(self, summary):
        """
        Speichert den aktuellen Spielzustand zusammen mit einer Zusammenfassung.

        Args:
        summary (str): Eine Beschreibung des aktuellen Spielzustands.
        """

        game_state_collection.add(
            documents=[{
                "round": self.round_number,
                "phase": self.phase,
                "summary": summary,
                "remaining_players": self.persistent_game_state['history']['remaining_players']
            }],
            ids=[str(uuid4())]
        )

    # Spielereignisse speichern
    def log_event(self, event_text, importance=0.8):
        """
        Speichert ein Spielereignis in der Ereignis-Sammlung.

        Args:
        event_text (str): Der Text, der das Ereignis beschreibt.
        importance (float): Die Wichtigkeit des Ereignisses (Standardwert: 0.8).
        """

        events_collection.add(
            documents=[{
                "game_event": event_text,
                "round": self.round_number,
                "importance": importance
            }],
            ids=[str(uuid4())]
        )

    def initialize_roles(self):
        """
        Initialisiert die Rollen der Spieler zufällig und speichert sie im persistenten Spielzustand.
        """

        roles = ['villager', 'villager', 'seer', 'werewolf', 'werewolf']
        random.shuffle(roles)
        self.persistent_game_state['players'] = {
            chr(65 + i): role for i, role in enumerate(roles)
        }
        self.persistent_game_state['history']['remaining_players'] = list(
            self.persistent_game_state['players'].keys()
        )
        for player in self.persistent_game_state['players'].keys():
            self.persistent_game_state['history']['last_statement'][player] = "None"

        print(f"Roles initialized: {self.persistent_game_state['players']}")

    def log_game_state(self):
        """
        Protokolliert den aktuellen Spielzustand in der Logdatei.
        """
        self.logger.info(f"Updated Game State: {self.persistent_game_state}")
        print(f"Updated Game State: {self.persistent_game_state}")

    def handle_night_phase(self):
        """
        Handhabt die Nachtphase des Spiels, einschließlich der Eliminierung eines Spielers durch Werwölfe.
        """

        print("Night phase started.")
        werewolves = [
            player for player, role in self.persistent_game_state['players'].items()
            if role == "werewolf"
        ]
        eliminated_player = None

        while not eliminated_player:
            for werewolf in werewolves:
                prompt = f"Player {werewolf}, suggest a villager to eliminate."
                suggestion = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": prompt}]
                ).choices[0].message.content.strip()

                # Speichere Vorschlag und Ereignis
                self.persistent_game_state['history']['last_statement'][werewolf] = suggestion
                self.persistent_game_state['history']['conversation_log'].append((werewolf, suggestion))
                self.log_event(f"{werewolf} suggested {suggestion}")

                # Check Consensus
                eliminated_player = self.check_for_consensus_gpt(
                    self.persistent_game_state['history']['conversation_log']
                )
                if eliminated_player:
                    break

        if eliminated_player in self.persistent_game_state['history']['remaining_players']:
            print(f"Final Decision: Player {eliminated_player} eliminated.")
            self.log_event(f"Player {eliminated_player} eliminated", importance=1.0)
            self.persistent_game_state['history']['remaining_players'].remove(eliminated_player)
            self.save_game_state(f"Player {eliminated_player} was eliminated.")
        else:
            print("Error: No valid target found.")
            self.logger.error("Error: No valid target found.")

    def check_for_consensus_gpt(self, conversation_log):
        """
        Überprüft mithilfe von GPT, ob ein Konsens in der Werwolf-Gruppe über die Eliminierung eines Spielers besteht.

        Args:
        conversation_log (list): Das Protokoll der Werwolf-Konversation.

        Returns:
        str: Der Name des Spielers, auf den sich die Gruppe geeinigt hat, oder None.
        """
        prompt = (
            f"Analyze the conversation log and count unique votes and agreements. "
            f"If at least one vote and one agreement exist for the same target, declare consensus.\n"
            f"Conversation Log:\n{conversation_log}"
        )

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}]
        ).choices[0].message.content.strip()

        match = re.search(r"Consensus reached on Player ([A-E])", response)
        if match:
            return match.group(1)
        return None

    def start_game(self):
        """
        Startet das Spiel, initialisiert Agenten und Rollen und beginnt mit der ersten Nachtphase.
        """
        print("Game started!")
        self.register_agents()
        self.initialize_roles()
        self.handle_night_phase()


# Spielstart
if __name__ == "__main__":
    controller = GameController()
    controller.start_game()
