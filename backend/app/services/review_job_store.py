from uuid import UUID, uuid4
from app.schemas.review_job import ReviewJob, ReviewJobStatus
from app.schemas.analysis import GameReviewResponse
from app.core.redis_client import redis_client

REVIEW_JOB_KEY_PREFIX = "review_job:"
REVIEW_JOB_TTL= 60 * 60 * 24  # 24 hours in seconds

def get_job_key(job_id: UUID) -> str:
    return f"{REVIEW_JOB_KEY_PREFIX}{job_id}"

def _save_review_job_to_redis(job: ReviewJob) -> None:
    serialized_job = job.model_dump_json()
    redis_client.setex(get_job_key(job.job_id), REVIEW_JOB_TTL, serialized_job)

def load_review_job(job_id: UUID) -> ReviewJob | None:
    job_key = get_job_key(job_id)
    stored_job = redis_client.get(job_key)

    if stored_job:
        return ReviewJob.model_validate_json(stored_job)
    
    return None

def create_review_job() -> ReviewJob:
    job = ReviewJob(
        job_id=uuid4(),
        status=ReviewJobStatus.QUEUED,
        completed_plies=0,
        total_plies=None,
        result=None,
        error=None
    )

    _save_review_job_to_redis(job)

    return job

def get_review_job(job_id: UUID) -> ReviewJob | None:
    return load_review_job(job_id)

def mark_review_job_running(job_id: UUID) -> None:
    job = load_review_job(job_id)

    if job is None:
        raise KeyError(f"Review job {job_id} not found")
    
    job.status = ReviewJobStatus.RUNNING
    job.error = None
    _save_review_job_to_redis(job)
    
    return

def mark_review_job_completed(job_id: UUID, result: GameReviewResponse) -> None:
    job = load_review_job(job_id)

    if job is None:
            raise KeyError(f"Review job {job_id} not found")
        
    job.status = ReviewJobStatus.COMPLETED
    job.error = None
    job.result = result

    _save_review_job_to_redis(job)

    return

def mark_review_job_failed(job_id: UUID, error: str) -> None:
    job = load_review_job(job_id)

    if job is None:
            raise KeyError(f"Review job {job_id} not found")
        
    job.status = ReviewJobStatus.FAILED
    job.error = error
    job.result = None

    _save_review_job_to_redis(job)

    return

def update_review_job_progress(job_id: UUID, completed_plies: int, total_plies: int) -> None:
    job = get_review_job(job_id)

    if job is None:
        raise KeyError(f"Review job {job_id} not found")

    if completed_plies < 0:
        raise ValueError("Completed plies cannot be negative")

    if total_plies < 0:
        raise ValueError("Total plies cannot be negative")

    if completed_plies > total_plies:
        raise ValueError(
            "Completed plies cannot exceed total plies"
        )

    job.completed_plies = completed_plies
    job.total_plies = total_plies

    _save_review_job_to_redis(job)

    return


