import random
from config import game_config

def generate_player_names(num_ai_players, human_player_name):
    """
    Generate player names: one human and randomly chosen AI names.

    Args:
        num_ai_players (int): Number of AI players.
        human_player_name (str): Name provided by the human player.

    Returns:
        list: Combined list of human and AI player names.
    """
    # Predefined list of 15 AI names
    ai_name_pool = [
        "AI_Alpha", "Bot_Bravo", "AI_Charlie", "Bot_Delta", "AI_Echo",
        "Bot_Foxtrot", "AI_Golf", "Bot_Hotel", "AI_India", "Bot_Juliet",
        "AI_Kilo", "Bot_Lima", "AI_Mike", "Bot_November", "AI_Oscar"
    ]

    # Randomly select AI names
    ai_names = random.sample(ai_name_pool, num_ai_players)

    # Combine human and AI player names
    return [human_player_name] + ai_names


def adjust_roles_for_players(num_players, roles):
    """
    Adjust roles dynamically based on the number of players.

    Args:
        num_players (int): Total number of players.
        roles (dict): The roles dictionary to adjust.

    Returns:
        dict: Updated roles with adjusted counts.
    """
    base_roles = {
        "werewolf": 2,
        "villager": 2,
        "hexe": 1,
        "seherin": 1,
        "amor": 1,
    }
    additional_roles = ["villager", "werewolf"]

    # Reset role counts to base values
    for role, count in base_roles.items():
        roles[role]["count"] = count

    # Add extra roles based on player count
    extra_players = num_players - game_config.MIN_AGENTS
    for i in range(extra_players):
        role_to_add = additional_roles[i % len(additional_roles)]
        roles[role_to_add]["count"] += 1

    return roles

def assign_roles(players, seed=42):
    """
    Assign roles to players dynamically based on the configuration.

    Args:
        players (list): List of player names.
        seed (int): Random seed for reproducibility.

    Returns:
        dict: Mapping of players to roles.
    """
    random.seed(seed)

    # Adjust roles based on the number of players
    num_players = len(players)
    updated_roles = adjust_roles_for_players(num_players, game_config.ROLES)

    # Prepare role pool
    role_pool = []
    for role, details in updated_roles.items():
        role_count = details["count"]
        if role_count:
            role_pool.extend([role] * role_count)

    # Shuffle roles
    random.shuffle(role_pool)

    # Assign roles to players
    assigned_roles = {player: role_pool.pop() for player in players}
    return assigned_roles

# Example usage
if __name__ == "__main__":
    human_name = input("Enter your name: ")
    players = generate_player_names(num_ai_players=10, human_player_name=human_name)
    print("Player Names:", players)

    assigned_roles = assign_roles(players)
    print("Assigned Roles:", assigned_roles)
