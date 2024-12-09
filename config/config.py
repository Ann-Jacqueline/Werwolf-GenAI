# config.py

class GameConfig:
    # Game Settings
    MIN_AGENTS = 7  # Minimum number of agents, including moderator
    MAX_MODERATOR = 1  # Maximum number of moderators (only 1)
    MIN_MODERATOR = 1  # Minimum number of moderators (only 1)
    MAX_HUMAN_PLAYER = 1  # Always include one human player
    ACTIVE_PLAYERS = 5  # Human + 4 AI players

    # Role Allocation
    MIN_DORFBEWOHNER = 2  # Minimum number of villagers
    MAX_SONDERROLLEN = 3  # Maximum number of special roles
    MIN_WEREWOLVES = 2  # Minimum number of werewolves
    MAX_WEREWOLVES = 4  # Maximum number of werewolves

    ROLES = {
        "villager": {"count": None},  # Calculated based on remaining slots
        "werewolf": {"count": 2},  # Default is 2; dynamically increased to 4 max
        "amor": {"count": 1},
        "hexe": {"count": 1},  # Hexe shares role with Jäger
        "seherin": {"count": 1},
    }

    # Moderator Settings
    MODERATOR_INSTANZ = "moderator"
    MODERATOR_DESCRIPTION = (
        "Der Moderator sorgt für einen reibungslosen Spielablauf und verwaltet die Spielmechanik."
    )

    # Night Action Sequence (Hardcoded)
    NIGHT_SEQUENCE = [
        "amor",  # Amor acts first
        "seherin",  # Seherin inspects a player
        "werewolf",  # Werewolves choose a victim
        "hexe",  # Hexe acts last
    ]

    # Role Descriptions
    ROLE_DESCRIPTIONS = {
        "villager": {
            "description": "Du bist ein Dorfbewohner. Dein Ziel ist es, die Werwölfe zu identifizieren und aus dem Dorf zu vertreiben.",
            "strategy": "Beobachte sorgfältig die Interaktionen der Spieler und achte auf verdächtiges Verhalten. Arbeite mit den anderen Dorfbewohnern zusammen, um fundierte Entscheidungen zu treffen.",
        },
        "werewolf": {
            "description": "Du bist ein Werwolf. Dein Ziel ist es, die Dorfbewohner heimlich zu eliminieren.",
            "strategy": "Verhalte dich tagsüber unauffällig und tue so, als wärst du ein Dorfbewohner. Arbeite nachts mit deinen Werwolf-Verbündeten zusammen, um strategisch Opfer auszuwählen.",
        },
        "amor": {
            "description": "Du bist Amor. In der ersten Nacht wählst du zwei Spieler aus, die sich verlieben. Wenn einer stirbt, stirbt auch der andere.",
            "strategy": "Wähle strategisch zwei Spieler aus, um Allianzen zu schmieden oder Spannungen im Spiel zu erzeugen. Überlege, wie deine Wahl den Spielverlauf beeinflussen könnte.",
        },
        "hexe": {
            "description": "Du bist die Hexe. Du besitzt einen Heiltrank und einen Gifttrank. Setze diese weise ein.",
            "strategy": "Beobachte sorgfältig, wann du den Heiltrank einsetzen solltest, um einen wichtigen Spieler zu retten, oder den Gifttrank, um einen verdächtigen Spieler zu eliminieren. Denke an die begrenzte Nutzung deiner Tränke.",
        },
        "seherin": {
            "description": "Du bist die Seherin. Jede Nacht kannst du einen Spieler überprüfen, um seine Rolle herauszufinden.",
            "strategy": "Sammle so viele Informationen wie möglich, ohne dich frühzeitig zu verraten. Lenke die Diskussionen am Tag subtil, um die Abstimmungen zu beeinflussen, ohne ein Ziel zu werden.",
        },
    }

    # Random Seed for Reproducibility
    RANDOM_SEED = 42

    # Device Settings
    DEVICE = "cuda"  # Use "cuda" for GPU or "cpu" for CPU


# Instantiate global configuration
game_config = GameConfig()
