from uuid import UUID, uuid4
import pytest
from redis import Redis
from app.schemas.review_job import ReviewJobStatus
from app.services import review_job_store

TEST_REDIS_URL = "redis://localhost:6379/15"

@pytest.fixture(scope="session")
def test_redis_client() -> Redis:
    client = Redis.from_url(TEST_REDIS_URL, decode_responses=True)

    client.ping()

    yield client

    client.close()

@pytest.fixture(autouse=True)
def use_test_redis(monkeypatch: pytest.MonkeyPatch, test_redis_client: Redis) -> None:
    test_redis_client.flushdb()

    monkeypatch.setattr(
        review_job_store,
        "redis_client",
        test_redis_client,
    )

    yield

def test_create_review_job_persists_job() -> None:
    created_job = review_job_store.create_review_job()

    loaded_job = review_job_store.get_review_job(
        created_job.job_id
    )

    assert loaded_job is not None
    assert loaded_job == created_job
    assert loaded_job is not created_job
    assert loaded_job.status == ReviewJobStatus.QUEUED
    assert loaded_job.completed_plies == 0
    assert loaded_job.total_plies is None
    assert loaded_job.result is None
    assert loaded_job.error is None


def test_get_review_job_returns_none_when_missing() -> None:
    assert (
        review_job_store.get_review_job(uuid4())
        is None
    )


def test_mark_review_job_running_persists_status() -> None:
    created_job = review_job_store.create_review_job()

    review_job_store.mark_review_job_running(
        created_job.job_id
    )

    loaded_job = review_job_store.get_review_job(
        created_job.job_id
    )

    assert loaded_job is not None
    assert loaded_job.status == ReviewJobStatus.RUNNING
    assert loaded_job.error is None


def test_update_review_job_progress_persists_progress() -> None:
    created_job = review_job_store.create_review_job()

    review_job_store.update_review_job_progress(
        job_id=created_job.job_id,
        completed_plies=12,
        total_plies=43,
    )

    loaded_job = review_job_store.get_review_job(
        created_job.job_id
    )

    assert loaded_job is not None
    assert loaded_job.completed_plies == 12
    assert loaded_job.total_plies == 43


@pytest.mark.parametrize(
    (
        "completed_plies",
        "total_plies",
    ),
    [
        (-1, 20),
        (10, -1),
        (21, 20),
    ],
)
def test_update_review_job_progress_rejects_invalid_values(
    completed_plies: int,
    total_plies: int,
) -> None:
    created_job = review_job_store.create_review_job()

    with pytest.raises(ValueError):
        review_job_store.update_review_job_progress(
            job_id=created_job.job_id,
            completed_plies=completed_plies,
            total_plies=total_plies,
        )


def test_mark_review_job_failed_persists_error() -> None:
    created_job = review_job_store.create_review_job()

    review_job_store.update_review_job_progress(
        job_id=created_job.job_id,
        completed_plies=8,
        total_plies=43,
    )

    review_job_store.mark_review_job_failed(
        job_id=created_job.job_id,
        error="Stockfish stopped unexpectedly",
    )

    loaded_job = review_job_store.get_review_job(
        created_job.job_id
    )

    assert loaded_job is not None
    assert loaded_job.status == ReviewJobStatus.FAILED
    assert (
        loaded_job.error
        == "Stockfish stopped unexpectedly"
    )
    assert loaded_job.result is None
    assert loaded_job.completed_plies == 8
    assert loaded_job.total_plies == 43


def test_created_job_has_expiration(
    test_redis_client: Redis,
) -> None:
    created_job = review_job_store.create_review_job()

    redis_key = review_job_store.get_job_key(
        created_job.job_id
    )

    ttl = test_redis_client.ttl(redis_key)

    assert ttl > 0
    assert (
        ttl
        <= review_job_store.REVIEW_JOB_TTL
    )