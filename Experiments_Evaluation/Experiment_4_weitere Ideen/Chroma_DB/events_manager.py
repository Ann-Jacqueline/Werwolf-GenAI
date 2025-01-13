# events_manager.py
"""
Verwaltung von Spielereignissen.

Dieses Modul bietet Funktionen zum Hinzufügen von Spielereignissen zur Ereignis-Sammlung.
"""

from chroma_client import events_collection
from uuid import uuid4

def add_game_event(event_text, round_number, importance):
    """
        Fügt ein neues Spielereignis zur Ereignis-Sammlung hinzu.

        Args:
            event_text (str): Der Text, der das Ereignis beschreibt.
            round_number (int): Die Rundennummer, in der das Ereignis stattfand.
            importance (float): Die Wichtigkeit des Ereignisses (zwischen 0 und 1).

        Returns:
            str: Eine eindeutige ID, die dem hinzugefügten Ereignis zugewiesen wurde.
        """
    event_id = str(uuid4())
    events_collection.add(
        documents=[{
            "game_event": event_text,
            "round": round_number,
            "importance": importance
        }],
        ids=[event_id]
    )
    return event_id
