from pydantic import BaseModel
from datetime import datetime
from enum import StrEnum

from app.schemas.analysis import GameSource

class ImportedGame(BaseModel):
    pgn: str
    source: GameSource
    external_id: str
    white: str
    black: str
    white_elo: int | None
    black_elo: int | None
    result: str
    played_at: datetime
    time_class: str

class ImportedGamesResponse(BaseModel):
    username: str
    source: GameSource
    games: list[ImportedGame]

class ImportedSource(StrEnum):
    CHESS_COM = "chess-com"
    LICHESS = "lichess"
