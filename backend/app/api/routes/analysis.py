from app.schemas.analysis import AnalysisRequest, AnalysisResponse, MoveReviewResponse, MoveReviewRequest, GameReviewRequest, GameReviewResponse
from app.services.engine import analyze_fen, review_move
from app.services.game_review import review_game
from fastapi import APIRouter

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
def analyze_position(analysis_request: AnalysisRequest):
    return analyze_fen(analysis_request.fen, analysis_request.depth)

@router.post("/move-review", response_model=MoveReviewResponse)
def move_review(move_review_request: MoveReviewRequest):
    return review_move(move_review_request.fen_before, move_review_request.move_uci, move_review_request.depth)

@router.post("/game-review", response_model=GameReviewResponse)
def game_review(game_review_request: GameReviewRequest):
    return review_game(game_review_request.pgn, game_review_request.depth)