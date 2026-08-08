def ability_modifier(score: int) -> int:
    """Calculate the D&D ability modifier for an ability score."""

    return (score - 10) // 2

def proficiency_bonus(level: int) -> int:
    """Calculate the proficiency bonus for a character level."""

    return 2 + (level - 1) // 4