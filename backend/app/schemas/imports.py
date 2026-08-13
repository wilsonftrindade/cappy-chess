from pydantic import BaseModel
from datetime import datetime

from app.schemas.analysis import GameSource

class ImportedGame(BaseModel):
    pgn: str
    external_id: str
    white: str
    black: str
    white_elo: int | None
    black_elo: int | None
    result: str
    played_at: datetime
    time_class: datetime

class ImportedGamesResponse(BaseModel):
    username: str
    sourece: GameSource
    games: list[ImportedGame]