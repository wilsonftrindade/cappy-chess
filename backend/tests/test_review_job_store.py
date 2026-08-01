from uuid import UUID, uuid4

import pytest

from app.schemas.review_job import ReviewJobStatus
from app.services import review_job_store

@pytest.fixture(autouse=True)
def empty_review_job_store(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        review_job_store,
        "_review_jobs",
        {},
    )

def test_create_review_job_stores_queued_job() -> None:
    job = review_job_store.create_review_job()

    assert isinstance(job.job_id, UUID)
    assert job.status == ReviewJobStatus.QUEUED
    assert job.completed_plies == 0
    assert job.total_plies is None
    assert job.result is None
    assert job.error is None

    retrieved_job = review_job_store.get_review_job(job.job_id)

    assert retrieved_job is not None
    assert retrieved_job.job_id == job.job_id
    assert retrieved_job.status == ReviewJobStatus.QUEUED

def test_get_review_job_returns_none_for_unknown_job() -> None:
    unknown_job_id = uuid4()

    job = review_job_store.get_review_job(unknown_job_id)

    assert job is None

def test_mark_review_job_running_changes_status() -> None:
    job = review_job_store.create_review_job()

    review_job_store.mark_review_job_running(job.job_id)

    assert job.status == ReviewJobStatus.RUNNING
    assert job.result is None
    assert job.error is None

    stored_job = review_job_store.get_review_job(
        job.job_id
    )

    assert stored_job is not None
    assert stored_job.status == ReviewJobStatus.RUNNING

def test_update_review_job_progress() -> None:
    job = review_job_store.create_review_job()

    review_job_store.mark_review_job_running(job.job_id)


    review_job_store.update_review_job_progress(
        job_id=job.job_id,
        completed_plies=12,
        total_plies=50,
    )


    assert job.status == ReviewJobStatus.RUNNING
    assert job.completed_plies == 12
    assert job.total_plies == 50

def test_mark_review_job_failed_stores_error() -> None:
    job = review_job_store.create_review_job()

    review_job_store.mark_review_job_running(job.job_id)

    review_job_store.update_review_job_progress(
        job_id=job.job_id,
        completed_plies=8,
        total_plies=40,
    )

    review_job_store.mark_review_job_failed(
        job_id=job.job_id,
        error="Stockfish stopped unexpectedly",
    )
    

    assert job.status == ReviewJobStatus.FAILED
    assert job.error == "Stockfish stopped unexpectedly"
    assert job.result is None

    assert job.completed_plies == 8
    assert job.total_plies == 40

def test_mark_review_job_running_raises_for_unknown_job() -> None:
    unknown_job_id = uuid4()

    with pytest.raises(KeyError):
        review_job_store.mark_review_job_running(
            unknown_job_id
        )