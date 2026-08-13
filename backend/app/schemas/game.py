from pydantic import BaseModel

class ParseGameRequest(BaseModel):
    pgn: str

class ParsedMove(BaseModel):
    move_number: int
    color: str
    move_san: str
    move_uci: str
    fen_before: str
    fen_after: str

class ParsedGameResponse(BaseModel):
    moves: list[ParsedMove]
    white: str
    black: str
    result: str
    white_elo: int | None
    black_elo: int | None