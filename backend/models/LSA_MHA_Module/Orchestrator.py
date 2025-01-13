import logging
from io import StringIO

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
        '''
         # Logging initialisieren
        logging.basicConfig(
            filename="game_log.txt",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        '''

        self.logger = logging.getLogger(__name__)

        # Global history initialization
        self.global_history = GlobalHistoryModel(self.logger)

        # Logging initialisieren
        self.log_stream = StringIO()  # Puffer für Logs
        log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # File handler (für game_log.txt)
        file_handler = logging.FileHandler("game_log.txt")
        file_handler.setFormatter(log_formatter)

        # Stream handler (für den Puffer)
        stream_handler = logging.StreamHandler(self.log_stream)
        stream_handler.setFormatter(log_formatter)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

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
            orchestrator=self,
            game_state=self.game_state,
            prompt_builder=self.prompt_builder,
            gpt_client=self.gpt_interaction,
            consensus_checker=self.consensus_checker,
            moderator=self.moderator,
            global_history=self.global_history,
            reflection=self.reflection,
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
            human_player = self.game_state.get_players_with_role()
            self.logger.info(f"Human Player {human_player} is up. Awaiting their argument.")

            # Aufforderung an das Frontend, Argument zu liefern
            self.global_history.record_event(
                "human_turn",
                {"message": f"Human Player {human_player}, please provide your argument."}
            )

    def check_game_end_conditions(self):
        """
        Checks if the game has reached an end condition.
        Ends the game if:
        - All werewolves are eliminated (Villagers win).
        - Werewolves equal or outnumber non-werewolves (Werewolves win).
        """
        remaining_players = self.game_state.get_remaining_players()
        werewolves = self.game_state.get_players_with_role("werewolf")
        villagers = [p for p in remaining_players if p not in werewolves]

        if len(werewolves) == 1:
            print("🎉 Congratulations Villagers! You have eliminated all the werewolves and kept your village safe!")
            print("GAME OVER. Villagers win!")
            exit(0)  # End the game
        elif len(villagers) == 1:
            print("😈 The Werewolves have taken over the village! All hope is lost!")
            print("GAME OVER. Werewolves win!")
            exit(0)  # End the game


# Beispielaufruf
if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.start_game()