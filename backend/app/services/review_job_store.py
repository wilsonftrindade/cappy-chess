from uuid import UUID, uuid4
from app.schemas.review_job import ReviewJob, ReviewJobStatus, ReviewJobCreatedResponse
from app.core.redis_client import redis_client
from app.core.redis_client import review_queue
from app.services.review_job_runner import run_review_job
from app.schemas.analysis import GameReviewResponse
from rq.job import Job, JobStatus, NoSuchJobError

JOB_TIMEOUT = 30 * 60  
JOB_RESULT_TTL = 60 * 60 * 24  
JOB_FAILURE_TTL = 60 * 60 * 1  

def get_review_job(job_id: UUID) -> ReviewJob | None:
    try:
        job = Job.fetch(str(job_id), connection=redis_client)

    except NoSuchJobError:
        return None

    job_status = map_rq_status(job.get_status(refresh=True))

    metadata = job.get_meta(refresh=True)

    result = None
    
    if (job_status == ReviewJobStatus.COMPLETED):
        raw_result = job.return_value()
        if raw_result is not None:
            result = GameReviewResponse.model_validate_json(raw_result)

    if (job_status == ReviewJobStatus.FAILED):
        raw_error = metadata.get("error")
        error = str(raw_error)

        if raw_error is None:
            error = "Game review failed"
    else:
        error = None

    completed_plies = metadata.get("completed_plies")
    total_plies = metadata.get("total_plies")

    return ReviewJob(
        job_id=job_id,
        status=job_status,
        completed_plies=completed_plies,
        total_plies=total_plies,
        result=result,
        error=error
    )


def enqueue_review_job(pgn: str, depth: int, review_id: UUID) -> ReviewJobCreatedResponse:
    review_queue.enqueue(
        run_review_job,
        review_id,
        pgn,
        depth,
        job_id=str(review_id),
        job_timeout=JOB_TIMEOUT,
        result_ttl=JOB_RESULT_TTL,
        failure_ttl=JOB_FAILURE_TTL,
        meta = {
            "completed_plies": 0,
            "total_plies": None,
            "error": None,
        }
    )
    
    return ReviewJobCreatedResponse(job_id=review_id, status=ReviewJobStatus.QUEUED)

def map_rq_status(job_status: object) -> JobStatus:

    if job_status in (JobStatus.QUEUED, JobStatus.SCHEDULED, JobStatus.DEFERRED, JobStatus.CREATED):
        return "queued"

    elif job_status == JobStatus.STARTED:
        return "running"

    elif job_status == JobStatus.FINISHED:
        return "completed"

    elif job_status in (JobStatus.FAILED, JobStatus.STOPPED, JobStatus.CANCELED ):
        return "failed"

    else:
        raise ValueError(f"Unknown RQ job status: {job_status.value}")

