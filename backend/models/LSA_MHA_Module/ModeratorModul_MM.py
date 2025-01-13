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

    def announce_elimination(self, eliminated_player, role, next_phase="day"):
        """
        Announces the elimination of a player and prepares for the next phase.
        """
        if not eliminated_player:
            announcement = "No player was eliminated this round."
            print(announcement)
            self.logger.info(announcement)
            if self.global_history:
                self.global_history.record_event("elimination", {"player": None, "role": None})
            return

        role_text = f"({role})" if role else "(Unknown role)"
        announcement = (
            f"During the night, Player {eliminated_player} {role_text} was eliminated by the werewolves. "
            f"Begin the {next_phase} discussions. Human, who would you eliminate next?"
        )
        self.logger.info(announcement)

        if self.global_history:
            self.global_history.record_event("elimination", {"player": eliminated_player, "role": role})
            self.global_history.add_to_log("Moderator", announcement)

        return announcement

    def comment_on_discussion(self, conversation_log, human_player=None):
        """
        Provides comments on the discussion based on the conversation log.
        """
        print("\n--- Moderator Comments ---")
        print("The discussion seems heated! Consider focusing on key points raised.")
        if any("suspicious" in statement for _, statement in conversation_log[-5:]):
            print("Suspicion is rising. Consider aligning your thoughts with the group.")
        if human_player:
            print(f"{human_player}, what do you think? Guide the discussion toward clarity.")
        else:
            print("Guide the discussion toward clarity.")
        print("--- End of Comments ---\n")

    def handle_phase_transition(self, phase, round_number):
        """
        Handles phase transition announcements.
        """
        self.announce_phase(phase, round_number)
        if phase == "night":
            print("Players, prepare for the night. Werewolves, make your decisions.")
        elif phase == "day":
            print("Players, it is day. Discuss and prepare for voting.")