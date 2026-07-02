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
