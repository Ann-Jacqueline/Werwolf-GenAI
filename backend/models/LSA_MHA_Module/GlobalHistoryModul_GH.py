import logging
from datetime import datetime
import json
import typing
class GlobalHistoryModel:
    """
    Global History Model (GH): Tracks the history of actions, decisions, and eliminations throughout the game.
    Temporarily stores data in memory until database integration is completed.
    """

    def __init__(self, logger=None, game_id=None):
        """
        Initialize the Global History Model.

        Args:
            logger (logging.Logger, optional): Logger instance for logging. Defaults to None.
            game_id (str, optional): Unique identifier for the game. Defaults to None.
        """
        self.history = []  # In-memory storage for game history
        self.logger = logger or logging.getLogger(__name__)
        self.game_id = game_id or f"game_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def record_event(self, event_type, details, metadata=None):
        """
        Records an event in the global history.

        Args:
            event_type (str): Type of event (e.g., "elimination", "vote", "phase_change").
            details (dict): Additional details about the event.
            metadata (dict, optional): Additional metadata (e.g., phase type). Defaults to None.
        """
        if not isinstance(details, dict):
            raise ValueError("Details must be a dictionary.")

        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details,
            "metadata": metadata or {}
        }
        self.history.append(event)
        self.logger.info(f"Event recorded: {event}")

    def get_recent_announcements(self, limit=5):
        """
        Fetches the most recent announcements from the global history.

        Args:
            limit (int): The maximum number of recent announcements to fetch. Defaults to 5.

        Returns:
            list: A list of recent announcement details.
        """
        return [
            event["details"]
            for event in reversed(self.history)
            if event["event_type"] == "elimination"
        ][:limit]

    def get_history(self, event_type=None):
        """
        Retrieves the entire history or filters by event type.

        Args:
            event_type (str, optional): Type of event to filter by. Defaults to None.

        Returns:
            list: List of matching events.
        """
        if event_type:
            return [event for event in self.history if event["event_type"] == event_type]
        return self.history

    def clear_history(self):
        """
        Clears the in-memory history (used for resetting between games).
        """
        self.history = []
        self.logger.info("Game history cleared.")

    def export_history(self, file_path):
        """
        Exports the history to a JSON file.

        Args:
            file_path (str): Path to save the exported file.
        """
        try:
            with open(file_path, "w") as file:
                json.dump(self.history, file, indent=4)
            self.logger.info(f"History exported to {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to export history: {e}")


    def sync_with_database(self, database_client):
        """
        Syncs the in-memory history and logs with a database.

        Args:
            database_client: Database client instance with a `write` method.

        Raises:
            ValueError: If the database client does not implement a `write` method.
        """
        if not hasattr(database_client, "write"):
            raise ValueError("Database client must have a 'write' method.")

        try:
            database_client.write({"history": self.history, "logs": self.logs})
            self.logger.info("History and logs successfully synced with the database.")
        except Exception as e:
            self.logger.error(f"Error during database sync: {e}")
            raise

    def deduplicate_events(self):
        """
        Removes duplicate events from the history.
        """
        unique_events = []
        seen = set()
        for event in self.history:
            event_id = (event["timestamp"], event["event_type"], json.dumps(event["details"], sort_keys=True))
            if event_id not in seen:
                seen.add(event_id)
                unique_events.append(event)
        self.history = unique_events
        self.logger.info("Duplicate events removed from history.")