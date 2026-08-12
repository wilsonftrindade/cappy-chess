from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from enum import StrEnum
from .analysis import GameReviewResponse

class ReviewJobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class ReviewJob(BaseModel):
    job_id: UUID
    status: ReviewJobStatus
    completed_plies: int
    total_plies: int | None
    result: GameReviewResponse | None
    error: str | None

class ReviewJobCreatedResponse(BaseModel):
    job_id: UUID
    status: ReviewJobStatus

class StoredReviewResponse(BaseModel):
    id: UUID
    game_id: UUID
    depth: int
    status: ReviewJobStatus
    result: GameReviewResponse | None
    error: str | None
    created_at: datetime
    completed_at: datetime | None
