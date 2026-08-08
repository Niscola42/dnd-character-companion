def ability_modifier(score: int) -> int:
    """Calculate the D&D ability modifier for an ability score."""

    return (score - 10) // 2

def proficiency_bonus(level: int) -> int:
    """Calculate the proficiency bonus for a character level."""

    if not 1 <= level <= 20:
        raise ValueError("level must be between 1 and 20")

    return 2 + (level - 1) // 4