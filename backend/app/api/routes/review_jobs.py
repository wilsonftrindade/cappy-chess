from email.policy import HTTP
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from app.schemas.review_job import ReviewJobCreatedResponse, ReviewJob
from app.schemas.analysis import GameReviewRequest
from app.services.review_job_store import get_review_job, enqueue_review_job

router = APIRouter()

@router.post("/review-jobs", response_model=ReviewJobCreatedResponse, status_code=status.HTTP_202_ACCEPTED)
def create_game_review_job(_request: GameReviewRequest):
    try:
        created_job_response = enqueue_review_job(_request.pgn, _request.depth)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not queue the review job",
        ) from exc

    return created_job_response

@router.get("/review-jobs/{job_id}", response_model=ReviewJob)
def get_game_review_job(job_id: UUID):
    job = get_review_job(job_id)

    if job is None:
        raise HTTPException(status_code=status.HTT, detail="Job not found")
    
    return job