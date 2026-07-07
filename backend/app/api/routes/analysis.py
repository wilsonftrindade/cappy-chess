from app.schemas.analysis import AnalysisRequest, AnalysisResponse, MoveReviewResponse, MoveReviewRequest
from app.services.engine import analyze_fen, review_move
from fastapi import APIRouter

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
def analyze_position(analysis_request: AnalysisRequest):
    return analyze_fen(analysis_request.fen, analysis_request.depth)

@router.post("/move-review", response_model=MoveReviewResponse)
def review(move_review_request: MoveReviewRequest):
    return review_move(move_review_request.fen_before, move_review_request.move_uci, move_review_request.depth)