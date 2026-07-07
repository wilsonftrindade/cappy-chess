from pydantic import BaseModel

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
    classification: str | None
