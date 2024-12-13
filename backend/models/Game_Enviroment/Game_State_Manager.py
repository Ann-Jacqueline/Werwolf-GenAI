class GameStateManager:
    def __init__(self):
        # Initialize persistent and tentative game states
        self.persistent_game_state = self._initialize_persistent_game_state()
        self.tentative_game_state = self._initialize_tentative_game_state()

    # Initialize Persistent Game State
    def _initialize_persistent_game_state(self):
        return {
            'players': {
                'A': 'Dorfbewohner',
                'B': 'Dorfbewohner',
                'C': 'Dorfbewohner',
                'D': 'Dorfbewohner',
                'E': 'Werwolf',
                'Agent': 'Werwolf'
            },
            'history': {
                "phase": {"night": 1, "day": 0},
                "lover": 0,
                "asleep": 1,
                "in_love": 0,
                "last_statement": {"Role": "Moderator", "Statement": "Die Nacht beginnt. Amor erwachen. Verliebte wählen."},
                "remaining_players": ["A", "B", "C", "D", "E"],
                "ally": ['E'],
                "target": [
                    {"ID": "A", "Role": "NULL"},
                    {"ID": "B", "Role": "NULL"},
                    {"ID": "C", "Role": "NULL"},
                    {"ID": "D", "Role": "NULL"}
                ],
                "past_rounds": []
            },
            'current_phase': {"round_number": 1, "phase": "night"},
            'ally': ['E'],
            'target': [
                {"ID": "C", "Role": "NULL"},
                {"ID": "D", "Role": "NULL"}
            ],
            'finds_me_suspicious': []
        }

    # Initialize Tentative Game State (Temporary Cache)
    def _initialize_tentative_game_state(self):
        return {
            "round_number": 1,
            "phase": "night",
            "llama_outputs": [],
            "agent_observations": [],
            "discussion_log": [],
            "voting_log": []
        }

    # Update Persistent Game State After a Round
    def finalize_round(self, summary, agent_outputs, agent_observations):
        round_summary = {
            "round_number": self.persistent_game_state['current_phase']['round_number'],
            "phase": self.persistent_game_state['current_phase']['phase'],
            "summary": summary,
            "agent_outputs": agent_outputs,
            "agent_observations": agent_observations
        }
        self.persistent_game_state['history']['past_rounds'].append(round_summary)
        self.increment_phase()

    # Clear Tentative Game State
    def clear_tentative_game_state(self):
        self.tentative_game_state = self._initialize_tentative_game_state()

    # Add Discussion Logs
    def add_to_discussion(self, output, observation):
        self.tentative_game_state['llama_outputs'].append(output)
        self.tentative_game_state['agent_observations'].append(observation)

    # Add Voting Logs
    def add_to_voting_log(self, log_entry):
        self.tentative_game_state['voting_log'].append(log_entry)

    # Increment Phase After Each Round
    def increment_phase(self):
        current_phase = self.persistent_game_state['current_phase']
        if current_phase['phase'] == 'night':
            current_phase['phase'] = 'day'
        else:
            current_phase['phase'] = 'night'
            current_phase['round_number'] += 1

    # Get Relevant Game State for Reflection Model
    def get_game_state_for_reflection(self, is_new_phase=False):
        if is_new_phase:
            return self.persistent_game_state
        return self.tentative_game_state
