import logging
from uuid import UUID, uuid4

from fastapi import HTTPException

from .game_review import review_game
from .review_job_store import mark_review_job_running, mark_review_job_completed, mark_review_job_failed, update_review_job_progress



logger = logging.getLogger(__name__)

def run_review_job(job_id: UUID, pgn: str, depth: int) -> None:
    mark_review_job_running(job_id)

    def progress_callback(completed_plies: int, total_plies: int) -> None:
        update_review_job_progress(job_id, completed_plies, total_plies)

    try: 
        reviewed_game = review_game(pgn, depth, progress_callback)
        mark_review_job_completed(job_id, reviewed_game)
        return
    except HTTPException as error:
        mark_review_job_failed(job_id, error.detail)
    except Exception as error:
        logger.exception("Unexpected error during review job %s", job_id)
        mark_review_job_failed(job_id, "Unexpected error while reviewing game")
        
    return


    



