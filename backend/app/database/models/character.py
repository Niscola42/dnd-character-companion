from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    SmallInteger,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base

from typing import Optional


class CharacterModel(Base):
    __tablename__ = "characters"
    __table_args__ = (
        CheckConstraint(
            "level BETWEEN 1 AND 5",
            name="ck_characters_level",
        ),
        CheckConstraint(
            """
            strength BETWEEN 1 AND 20
            AND dexterity BETWEEN 1 AND 20
            AND constitution BETWEEN 1 AND 20
            AND intelligence BETWEEN 1 AND 20
            AND wisdom BETWEEN 1 AND 20
            AND charisma BETWEEN 1 AND 20
            """,
            name="ck_characters_ability_scores",
        ),
        CheckConstraint(
            "maximum_hp > 0",
            name="ck_characters_maximum_hp",
        ),
        CheckConstraint(
            "current_hp BETWEEN 0 AND maximum_hp",
            name="ck_characters_current_hp",
        ),
        CheckConstraint(
            "temporary_hp >= 0",
            name="ck_characters_temporary_hp",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    level: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )
    character_class: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    portrait_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    strength: Mapped[int] = mapped_column(SmallInteger)
    dexterity: Mapped[int] = mapped_column(SmallInteger)
    constitution: Mapped[int] = mapped_column(SmallInteger)
    intelligence: Mapped[int] = mapped_column(SmallInteger)
    wisdom: Mapped[int] = mapped_column(SmallInteger)
    charisma: Mapped[int] = mapped_column(SmallInteger)

    maximum_hp: Mapped[int] = mapped_column(
        Integer,
        server_default="1",
        nullable=False,
    )
    current_hp: Mapped[int] = mapped_column(
        Integer,
        server_default="1",
        nullable=False,
    )
    temporary_hp: Mapped[int] = mapped_column(
        Integer,
        server_default="0",
        nullable=False,
    )

    saving_throw_proficiencies: Mapped[list[str]] = (
        mapped_column(
            JSON,
            default=list,
            nullable=False,
        )
    )
    skill_proficiencies: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    spellcasting_ability: Mapped[Optional[str]] = (
        mapped_column(
            String(20),
            nullable=True,
        )
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

