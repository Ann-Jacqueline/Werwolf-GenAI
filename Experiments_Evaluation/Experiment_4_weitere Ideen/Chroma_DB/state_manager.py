# state_manager.py
"""
Verwaltung von Spielzuständen.

Dieses Modul enthält Funktionen zum Speichern von Spielzuständen in der entsprechenden Sammlung.
"""

from chroma_client import game_state_collection
from uuid import uuid4

def save_game_state(game_state):
    """
        Speichert den aktuellen Spielzustand in der Spielzustand-Sammlung.

        Args:
            game_state (dict): Der aktuelle Zustand des Spiels als Dictionary.

        Returns:
            str: Eine eindeutige ID, die dem gespeicherten Spielzustand zugewiesen wurde.
        """
    state_id = str(uuid4())
    game_state_collection.add(
        documents=[game_state],
        ids=[state_id]
    )
    return state_id
