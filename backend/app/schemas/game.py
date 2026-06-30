from pydantic import BaseModel
from typing import Optional

class ParseGameRequest(BaseModel):
    pgn: str

class ParsedMove(BaseModel):
    move_number: int
    color: str
    san: str
    uci: str
    fen_before: str
    fen_after: str

class ParsedGameResponse(BaseModel):
    moves: list[ParsedMove]
    white: str
    black: str
    result: str
    white_elo: Optional[int]
    black_elo: Optional[int]