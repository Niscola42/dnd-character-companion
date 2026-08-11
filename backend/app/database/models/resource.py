from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class ResourceModel(Base):
    __tablename__ = "resources"
    __table_args__ = (
        CheckConstraint(
            "maximum > 0",
            name="ck_resources_maximum",
        ),
        CheckConstraint(
            "current BETWEEN 0 AND maximum",
            name="ck_resources_current",
        ),
        CheckConstraint(
            """
            recovery_type IN (
                'SHORT_REST',
                'LONG_REST',
                'MANUAL'
            )
            """,
            name="ck_resources_recovery_type",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    maximum: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    current: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    recovery_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    resource_metadata: Mapped[dict[str, object]] = (
        mapped_column(
            "metadata",
            JSON,
            default=dict,
            nullable=False,
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