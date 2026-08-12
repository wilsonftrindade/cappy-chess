import logging
from datetime import datetime, timezone
from uuid import UUID
from rq import get_current_job
from .game_review import review_game
from app.schemas.review_job import ReviewJobStatus
from app.core.database import SessionLocal
from app.models.review import Review


logger = logging.getLogger(__name__)

def run_review_job(job_id: UUID, pgn: str, depth: int) -> str:
    rq_job = get_current_job()

    if rq_job is None:
        raise RuntimeError("run_review_job must execute inside an RQ worker")

    def progress_callback(completed_plies: int, total_plies: int) -> None:
        rq_job.meta["completed_plies"] = completed_plies
        rq_job.meta["total_plies"] = total_plies
        rq_job.save_meta()

    try: 
        with SessionLocal.begin() as session:
            review = session.get(Review, job_id)
            if review is None:
                raise RuntimeError(f"Review {job_id} not found")
            
            review.status = ReviewJobStatus.RUNNING
            session.commit()

        reviewed_game = review_game(pgn, depth, progress_callback)

        with SessionLocal.begin() as session:
            review = session.get(Review, job_id)

            if review is None:
                raise RuntimeError(f"Review {job_id} not found")

            review.status = ReviewJobStatus.COMPLETED
            review.result_json = reviewed_game.model_dump(mode="json")
            review.completed_at = datetime.now(timezone.utc)
            review.error = None

        return reviewed_game.model_dump_json()

    except Exception as error:
        rq_job.meta["error"] = str(error)
        rq_job.save_meta()

        # if exception raised due to database availability
        try:
            with SessionLocal.begin() as session:
                review = session.get(Review, job_id)
                if review is not None:
                    review.status = ReviewJobStatus.FAILED
                    review.error = str(error)
        except Exception:
            logger.exception("Could not persist failed status for review %s", job_id)

        logger.exception("Unexpected error during review job %s", job_id)
        raise

    



