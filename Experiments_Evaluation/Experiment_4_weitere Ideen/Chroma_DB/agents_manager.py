# agents_manager.py
"""
Agentenmanagement.

Dieses Modul enthält Funktionen zum Hinzufügen von Agenten zu einer ChromaDB-Sammlung.
"""


from chroma_client import agents_collection
from uuid import uuid4

def add_agent(role, name):
    """
        Fügt einen neuen Agenten mit einer Rolle und einem Namen zur Agenten-Sammlung hinzu.

        Args:
            role (str): Die Rolle des Agenten (z. B. 'werewolf', 'seer').
            name (str): Der Name des Agenten.

        Returns:
            str: Eine eindeutige ID, die dem hinzugefügten Agenten zugewiesen wurde.
        """
    agent_id = str(uuid4())
    agents_collection.add(
        documents=[{"role": role, "name": name}],
        ids=[agent_id]
    )
    return agent_id
