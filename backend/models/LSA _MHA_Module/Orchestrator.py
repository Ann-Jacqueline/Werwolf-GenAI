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

        # Global history initialization
        self.global_history = GlobalHistoryModel(self.logger)

        # Module initialisieren
        self.game_state = GameState()
        self.prompt_builder = PromptBuilder(global_history=self.global_history)
        self.reflection = Reflection(self.game_state.to_dict())
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
            self.global_history,
            self.reflection,
            logger=self.logger
        )

        self.round_number = 1
        self.phase = "night"  # Startphase

    def initialize_game(self):
        """
        Initialisiert das Spiel, inklusive Rollen und Strategien.
        """
        player_ids = ['A', 'B', 'C', 'D', 'E']
        strategies = self.reflection.get_all_strategies()

        # Ensure game state initializes correctly
        self.game_state.initialize_roles(player_ids, strategies)
        self.logger.info("Game initialized with roles and strategies.")
        self.global_history.record_event(
            "game_initialized",
            {"players": player_ids, "strategies": strategies}
        )

    def handle_phase(self):
        """
        Handles the current phase (night or day) and transitions between phases.
        """
        try:
            eliminated_player = "No Elimination"  # Default value

            if self.phase == "night":
                self.moderator.handle_phase_transition("night", self.round_number)
                eliminated_player = self.voting.night_phase(self.round_number)

                if eliminated_player != "No Elimination":
                    self.global_history.record_event(
                        "elimination", {"player": eliminated_player, "phase": "night"}
                    )
                    self.moderator.announce_elimination(
                        eliminated_player,
                        self.game_state.get_role(eliminated_player)
                    )
                self.phase = "day"

            elif self.phase == "day":
                self.moderator.handle_phase_transition("day", self.round_number)
                self.moderator.comment_on_discussion(
                    conversation_log=self.game_state.global_conversation_log,
                    human_player="Human"
                )
                eliminated_player = self.voting.day_phase(eliminated_player, self.round_number)

                if eliminated_player != "No Elimination":
                    self.global_history.record_event(
                        "elimination", {"player": eliminated_player, "phase": "day"}
                    )
                    self.moderator.announce_elimination(
                        eliminated_player,
                        self.game_state.get_role(eliminated_player)
                    )
                self.phase = "night"
                self.round_number += 1

        except Exception as e:
            self.logger.error(f"Error during phase handling: {e}")
            print(f"Error encountered: {e}")

    def start_game(self):
        """
        Startet das Spiel und führt den Hauptspielzyklus aus.
        """
        print("Game started!")
        self.logger.info("Game started!")
        self.initialize_game()

        while True:
            self.handle_phase()

    def handle_conversation(self, player_id, prompt, statement):
        """
        Handles conversation for a specific player during the active phase.

        Args:
            player_id (str): The player ID.
            prompt (str): The prompt to present to the player.
            statement (str): The player's generated response.
        """
        # Log the prompt for debugging
        self.logger.debug(f"Prompt for Player {player_id}: {prompt}")

        # Log the player's statement and update their conversation log
        self.game_state.add_to_conversation_log(player_id, statement)
        self.logger.info(f"Player {player_id} responded: {statement}")

        # Only update the local log if the player is awake
        if self.game_state.players[player_id]["awake"]:
            local_log = self.game_state.get_conversation_log(player_id)  # Pass the player_id
            self.logger.info(f"Local log for {player_id}: {local_log}")


# Beispielaufruf
if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.start_game()
