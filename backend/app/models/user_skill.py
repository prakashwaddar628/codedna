from datetime import datetime
from sqlalchemy import ForeignKey, Integer, DateTime, func, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class UserSkill(Base):
    __tablename__ = "user_skills"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    confidence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
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

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_skills",
    )
    
    skill: Mapped["Skill"] = relationship(
        "Skill",
        back_populates="user_skills",
    )

    __table_args__ = (
        CheckConstraint("level >= 1 AND level <= 10", name="chk_user_skills_level"),
        CheckConstraint("confidence >= 1 AND confidence <= 10", name="chk_user_skills_confidence"),
        UniqueConstraint("user_id", "skill_id", name="uq_user_skill"),
    )
