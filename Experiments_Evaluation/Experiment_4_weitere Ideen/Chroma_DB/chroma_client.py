# chroma_client.py
"""
ChromaDB-Client Initialisierung und Sammlungsmanagement.

Dieses Modul bietet die Konfiguration und Initialisierung eines ChromaDB-Clients mit DuckDB+Parquet
sowie die Erstellung und Verwaltung von Sammlungen für Agenten, Spielereignisse und Spielzustände.
"""

import chromadb
from chromadb.config import Settings

# ChromaDB-Client Initialisierung
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_storage"
))

# Sammlungen erstellen
agents_collection = client.create_collection(name="agents")
events_collection = client.create_collection(name="game_events")
game_state_collection = client.create_collection(name="game_states")
