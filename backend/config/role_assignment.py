import random
from backend.config.config import game_config

def assign_roles(players, seed=42):
    """
    Assign roles to players dynamically based on the configuration in game_config.

    Args:
        players (list): List of player names.
        seed (int): Random seed for reproducibility.

    Returns:
        dict: Mapping of players to roles.
    """
    random.seed(seed)

    # Prepare role pool
    role_pool = []
    for role, details in game_config.ROLES.items():
        role_count = details["count"]
        if role_count:
            role_pool.extend([role] * role_count)

    # Dynamically calculate villagers (remaining roles)
    villager_count = len(players) - len(role_pool)
    if villager_count > 0:
        role_pool.extend(["villager"] * villager_count)

    # Shuffle roles
    random.shuffle(role_pool)

    # Assign roles to players
    assigned_roles = {player: role_pool.pop() for player in players}
    return assigned_roles

# Example usage
if __name__ == "__main__":
    players = ["Player1", "Player2", "Player3", "Player4", "Player5", "Player6", "Player7"]
    assigned_roles = assign_roles(players)
    print("Assigned Roles:", assigned_roles)
