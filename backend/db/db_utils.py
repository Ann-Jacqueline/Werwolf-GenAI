import sqlite3
import os

# Path to the database
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'werwolf.db')
DB_PATH = os.path.abspath(DB_PATH)  # Ensure it's an absolute path
print(f"DEBUG: Database path is {DB_PATH}")


def connect_to_db():
    """
    Establishes a connection to the database.
    """
    return sqlite3.connect(DB_PATH)
