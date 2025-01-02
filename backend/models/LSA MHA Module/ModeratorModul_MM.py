import logging


class Moderator:
    """
    Handles announcements, phase transitions, and game narrative management.
    """

    def __init__(self, logger=None, global_history=None):
        self.logger = logger or logging.getLogger(__name__)
        self.global_history = global_history

    def announce_phase(self, phase, round_number):
        """
        Announces the start of a new phase.
        """
        announcement = f"Starting {phase.capitalize()} Phase for Round {round_number}."
        print(announcement)
        self.logger.info(announcement)

        if self.global_history:
            self.global_history.record_event("phase_start", {
                "phase": phase,
                "round_number": round_number
            })

    def announce_elimination(self, eliminated_player, role):
        """
        Announces the elimination of a player.
        """
        if not eliminated_player:
            print("No player eliminated this round.")
            return

        role_text = f"({role})" if role else "(Unknown role)"
        announcement = f"Player {eliminated_player} {role_text} has been eliminated."
        print(announcement)
        self.logger.info(announcement)

        if self.global_history:
            self.global_history.record_event("elimination", {
                "player": eliminated_player,
                "role": role
            })

    def handle_phase_transition(self, phase, round_number):
        """
        Handles phase transition announcements.
        """
        self.announce_phase(phase, round_number)
        if phase == "night":
            print("Players, prepare for the night. Werewolves, make your decisions.")
        elif phase == "day":
            print("Players, it is day. Discuss and prepare for voting.")

