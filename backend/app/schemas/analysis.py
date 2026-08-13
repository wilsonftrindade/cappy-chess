from pydantic import BaseModel
from enum import StrEnum

class AnalysisRequest(BaseModel):
    fen: str
    depth: int

class AnalysisResponse(BaseModel):
    fen: str
    best_move_uci: str | None
    best_move_san: str | None
    evaluation_cp: int | None
    mate_in: int | None
    main_variation: list[str] | None

class MoveReviewRequest(BaseModel):
    fen_before: str
    move_uci: str
    depth: int

class MoveReviewResponse(BaseModel):
    fen_before: str
    move_uci: str
    move_san: str | None
    best_move_uci: str | None
    best_move_san: str | None
    eval_cp_before: int | None
    eval_cp_after: int | None
    eval_cp_loss: int | None
    mate_in_before: int | None
    mate_in_after: int | None
    win_probability_before: float | None
    win_probability_after: float | None
    win_probability_loss: float | None
    classification: str | None
    move_accuracy: float | None

class GameSource(StrEnum):
    MANUAL = "manual"
    CHESS_COM = "chess_com"
    LICHESS = "lichess"

class GameReviewRequest(BaseModel):
    pgn: str
    depth: int
    source: GameSource = GameSource.MANUAL
    external_id: str | None = None

class ReviewedMove(MoveReviewResponse):
    move_number: int
    color: str
    fen_after: str

class PlayerReviewSummary(BaseModel):
    move_count: int
    accuracy: float | None
    classification_counts: dict[str, int]
    
class GameReviewResponse(BaseModel):
    white: str
    black: str
    result: str
    white_elo: int | None
    black_elo: int | None
    reviewed_moves: list[ReviewedMove]
    white_summary: PlayerReviewSummary 
    black_summary: PlayerReviewSummary













