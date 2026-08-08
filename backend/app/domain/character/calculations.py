def ability_modifier(score: int) -> int:
    """Calculate the D&D ability modifier for an ability score."""

    return (score - 10) // 2