import logging
from GameStateModul_GS import GameState
from PromptBuilder_PB import PromptBuilder
from ReflectionModul_RM import Reflection
from GPTInteractionModul_GPT import GPTInteraction
from VotingModul_VM import VotingModule
from ModeratorModul_MM import Moderator
from GlobalHistoryModul_GH import GlobalHistoryModel
from ConsensusCheckerModul_CC import ConsensusChecker


class Orchestrator:
    """
    Orchestrator-Modul: Koordiniert die gesamte Spielmechanik und ruft die entsprechenden Module auf.
    """

    def __init__(self):
        # Logging initialisieren
        logging.basicConfig(
            filename="game_log.txt",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

        # Module initialisieren
        self.game_state = GameState()
        self.prompt_builder = PromptBuilder()
        self.reflection = Reflection(self.game_state.to_dict())  # Pass dictionary-like data
        self.gpt_interaction = GPTInteraction(self.logger)
        self.moderator = Moderator(self.logger)
        self.consensus_checker = ConsensusChecker(
            gpt_interaction=self.gpt_interaction,
            prompt_builder=self.prompt_builder,
            logger=self.logger
        )
        self.global_history = GlobalHistoryModel(self.logger)
        self.voting = VotingModule(
            self.game_state,
            self.prompt_builder,
            self.gpt_interaction,
            self.consensus_checker,
            self.moderator,
            self.global_history
        )

        # Spielstatus
        self.round_number = 1
        self.phase = "night"  # Startphase

    def initialize_game(self):
        """
        Initialisiert das Spiel, inklusive Rollen und Strategien.
        """
        player_ids = ['A', 'B', 'C', 'D', 'E']  # Beispiel-Spielerkennungen
        strategies = self.reflection.get_all_strategies()  # Strategien für alle Rollen holen
        self.game_state.initialize_roles(player_ids, strategies)  # Rollen und Strategien initialisieren
        self.logger.info("Game initialized with roles and strategies.")
        self.global_history.record_event("game_initialized", {"players": player_ids, "strategies": strategies})

    def handle_phase(self):
        """
        Handles the current phase (night or day) and transitions between phases.
        """
        try:
            eliminated_player = None  # Ensure `eliminated_player` is always defined

            if self.phase == "night":
                self.moderator.handle_phase_transition("night", self.round_number)
                eliminated_player = self.voting.night_phase(self.round_number)

                if eliminated_player:
                    self.global_history.record_event("elimination", {"player": eliminated_player, "phase": "night"})
                    self.moderator.announce_elimination(
                        eliminated_player,
                        self.game_state.get_role(eliminated_player)
                    )
                else:
                    eliminated_player = "No Elimination"

                self.phase = "day"  # Transition to day phase

            if self.phase == "day":
                self.moderator.handle_phase_transition("day", self.round_number)

                # Ensure `eliminated_player` has a valid value
                if not eliminated_player:
                    eliminated_player = "No Elimination"

                self.voting.day_phase(eliminated_player, self.round_number)
                self.global_history.record_event("discussion", {"phase": "day"})

                self.phase = "night"  # Transition to night phase
                self.round_number += 1  # Increment round number

        except Exception as e:
            self.logger.error(f"Error during phase handling: {e}")
            print(f"Error encountered: {e}")

    def start_game(self):
        """
        Startet das Spiel und führt den Hauptspielzyklus aus.
        """
        print("Game started!")
        self.logger.info("Game started!")

        # Initialisierung der Rollen und Strategien über GameState und Reflection
        self.initialize_game()

        # Spielzyklus starten
        while True:
            self.handle_phase()




# Beispielaufruf
if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.start_game()
