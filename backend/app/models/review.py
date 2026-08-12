from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class Review(Base):
  __tablename__ = "reviews"

  id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
  game_id: Mapped[UUID] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), nullable=False, index=True)
  depth: Mapped[int] = mapped_column(Integer, nullable=False)
  status: Mapped[str] = mapped_column(String(20), nullable=False, default="queued")
  result_json: Mapped[str | None] = mapped_column(JSONB, nullable=True)
  error: Mapped[str | None] = mapped_column(Text, nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
  game: Mapped["Game"] = relationship(back_populates="reviews")
