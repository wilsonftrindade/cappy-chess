from uuid import UUID, uuid4
from app.schemas.review_job import ReviewJob, ReviewJobStatus
from app.schemas.analysis import GameReviewResponse

_review_jobs: dict[UUID, ReviewJob] = {}

def create_review_job() -> ReviewJob:
    job = ReviewJob(
        job_id=uuid4(),
        status=ReviewJobStatus.QUEUED,
        completed_plies=0,
        total_plies=None,
        result=None,
        error=None
    )
    _review_jobs[job.job_id] = job

    return job

def get_review_job(job_id: UUID) -> ReviewJob | None:
    return _review_jobs.get(job_id)

def mark_review_job_running(job_id: UUID) -> None:
    job = _review_jobs.get(job_id)

    if job is None:
        raise KeyError(f"Review job {job_id} not found")
    
    job.status = ReviewJobStatus.RUNNING
    job.error = None
    return

def mark_review_job_completed(job_id: UUID, result: GameReviewResponse) -> None:
    job = _review_jobs.get(job_id)

    if job is None:
            raise KeyError(f"Review job {job_id} not found")
        
    job.status = ReviewJobStatus.COMPLETED
    job.error = None
    job.result = result

    return

def mark_review_job_failed(job_id: UUID, error: str) -> None:
    job = _review_jobs.get(job_id)

    if job is None:
            raise KeyError(f"Review job {job_id} not found")
        
    job.status = ReviewJobStatus.FAILED
    job.error = error
    job.result = None
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
    return


