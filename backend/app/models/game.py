from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class Game(Base):
  __tablename__ = "games"

  id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
  pgn: Mapped[str] = mapped_column(Text, nullable=False)
  white_name: Mapped[str] = mapped_column(String(100), nullable=False)
  black_name: Mapped[str] = mapped_column(String(100), nullable=False)
  white_elo: Mapped[int | None] = mapped_column(Integer, nullable=True)
  black_elo: Mapped[int | None] = mapped_column(Integer, nullable=True)
  result: Mapped[str] = mapped_column(String(10), nullable=False)
  source: Mapped[str] = mapped_column(String(20), nullable=False, default="manual")
  external_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  reviews: Mapped[list["Review"]] = relationship(back_populates="game", cascade="all, delete-orphan")




  
