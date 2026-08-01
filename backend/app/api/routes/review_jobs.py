from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from app.schemas.review_job import ReviewJobCreatedResponse, ReviewJob
from app.schemas.analysis import GameReviewRequest
from app.services.review_job_store import create_review_job, get_review_job
from app.services.review_job_runner import run_review_job

router = APIRouter()

@router.post("/review-jobs", response_model=ReviewJobCreatedResponse, status_code=status.HTTP_202_ACCEPTED)
def create_game_review_job(_request: GameReviewRequest, background_tasks: BackgroundTasks):
    job = create_review_job()

    background_tasks.add_task(
        run_review_job,
        job.job_id,
        _request.pgn,
        _request.depth
    )
    return ReviewJobCreatedResponse(job_id=job.job_id, status=job.status)

@router.get("/review-jobs/{job_id}", response_model=ReviewJob)
def get_game_review_job(job_id: UUID):
    job = get_review_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job