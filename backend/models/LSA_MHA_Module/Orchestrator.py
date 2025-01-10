import sys
from io import StringIO
import logging
from .GameStateModul_GS import GameState
from .PromptBuilder_PB import PromptBuilder
from .ReflectionModul_RM import Reflection
from .GPTInteractionModul_GPT import GPTInteraction
from .VotingModul_VM import VotingModule
from .ModeratorModul_MM import Moderator
from .GlobalHistoryModul_GH import GlobalHistoryModel
from .ConsensusCheckerModul_CC import ConsensusChecker

class Orchestrator:
    def __init__(self):
        # Redirect stdout to capture terminal outputs
        self.terminal_output = StringIO()
        sys.stdout = self.terminal_output

        # Main logger for detailed logs
        self.logger = logging.getLogger("main_logger")
        self.logger.setLevel(logging.INFO)
        log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # File handler for detailed logs
        file_handler = logging.FileHandler("game_log.txt")
        file_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)

        # Stream handler for in-memory logs
        stream_handler = logging.StreamHandler(self.terminal_output)
        stream_handler.setFormatter(log_formatter)
        self.logger.addHandler(stream_handler)

        # Stripped logger for frontend (simplified logs)
        self.stripped_logger = logging.getLogger("stripped_logger")
        self.stripped_logger.setLevel(logging.INFO)
        stripped_file_handler = logging.FileHandler("stripped_game_log.txt")
        stripped_file_handler.setFormatter(logging.Formatter("%(message)s"))  # Simplified format
        self.stripped_logger.addHandler(stripped_file_handler)

        # Module initializations
        self.global_history = GlobalHistoryModel(self.logger)
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
        self.phase = "night"  # Starting phase

    def log_gpt_response(self, response):
        """
        Logs only the clean GPT response.
        """
        self.logger.info(response)

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

    def log_to_terminal(self, message):
        """
        Prints a message to the terminal (captured in the buffer).
        """
        print(message)
        self.logger.info(message)  # Log to the main logger
        self.stripped_logger.info(message)  # Log stripped version for frontend

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

    def log_event(self,message):
        """
        Loggt ein Ereignis in das GHM und gibt es in Konsole aus
        """
        self.logger.info(message)
        self.global_history.record_event("log", {"message": message})

    def handle_human_player_turn(self):
            """
            Logik für die Interaktion mit dem Human Player.
            """
            human_player = self.game_state.get_human_player()
            self.logger.info(f"Human Player {human_player} is up. Awaiting their argument.")

            # Aufforderung an das Frontend, Argument zu liefern
            self.global_history.record_event(
                "human_turn",
                {"message": f"Human Player {human_player}, please provide your argument."}
            )


# Beispielaufruf
if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.start_game()
