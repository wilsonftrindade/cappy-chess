import logging
from typing import Any
from uuid import UUID
from rq import get_current_job
from .game_review import review_game

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
        reviewed_game = review_game(pgn, depth, progress_callback)

    except Exception as error:
        rq_job.meta["error"] = str(error)
        rq_job.save_meta()
        logger.exception("Unexpected error during review job %s", job_id)
        raise

    return reviewed_game.model_dump_json()
    



