from app.schemas.analysis import AnalysisRequest, AnalysisResponse, GameReviewResponse
from app.schemas.review_job import StoredReviewResponse
from app.services.engine import analyze_fen
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.review import Review

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
def analyze_position(analysis_request: AnalysisRequest):
    return analyze_fen(analysis_request.fen, analysis_request.depth)

@router.get("/reviews/{review_id}", response_model=StoredReviewResponse)
def get_review(review_id: str, db: Session = Depends(get_db)):
    review = db.get(Review, review_id)

    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    result = None
    if review.result_json is not None:
        result = GameReviewResponse.model_validate(review.result_json)

    response = StoredReviewResponse(
        id=review.id,
        game_id=review.game_id,
        depth=review.depth,
        status=review.status,
        result=result,
        error=review.error,
        created_at=review.created_at,
        completed_at=review.completed_at
    )

    return response

    




