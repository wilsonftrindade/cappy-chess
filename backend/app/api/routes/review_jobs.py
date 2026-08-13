from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.review_job import ReviewJobCreatedResponse, ReviewJob, ReviewJobStatus
from app.schemas.analysis import GameReviewRequest
from app.services.review_job_store import get_review_job, enqueue_review_job
from app.services.review_persistance import get_or_create_game_and_review
from app.core.database import get_db

router = APIRouter()

@router.post("/review-jobs", response_model=ReviewJobCreatedResponse, status_code=status.HTTP_202_ACCEPTED)
def create_game_review_job(_request: GameReviewRequest, db: Session = Depends(get_db)):
    review, created = get_or_create_game_and_review(db, _request.pgn, _request.depth)

    # return the existing review id and status from Postgres
    if not created:
        return ReviewJobCreatedResponse(job_id=review.id, status=review.status)
   
    try:
        created_job_response = enqueue_review_job(_request.pgn, _request.depth, review.id)
        
    except Exception as exc:
        review.status = ReviewJobStatus.FAILED
        review.error = f"Could not enqueue review job: {exc}"
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not queue the review job",
        ) from exc

    return created_job_response

@router.get("/review-jobs/{job_id}", response_model=ReviewJob)
def get_game_review_job(job_id: UUID):
    job = get_review_job(job_id)

    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    return job