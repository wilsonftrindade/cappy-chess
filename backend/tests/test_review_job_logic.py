from unittest.mock import MagicMock
from uuid import uuid4, UUID

import pytest
from rq.job import JobStatus

from app.schemas.review_job import ReviewJobStatus
from app.services import review_job_store
from app.services import review_job_runner


def test_run_review_job_updates_progress_and_returns_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rq_job = MagicMock()
    rq_job.meta = {}

    reviewed_game = MagicMock()
    reviewed_game.model_dump_json.return_value = (
        '{"reviewed_moves":[]}'
    )

    def fake_review_game(
        pgn: str,
        depth: int,
        progress_callback,
    ):
        assert pgn == "test-pgn"
        assert depth == 17

        progress_callback(0, 43)
        progress_callback(12, 43)

        return reviewed_game

    monkeypatch.setattr(
        review_job_runner,
        "get_current_job",
        lambda: rq_job,
    )
    monkeypatch.setattr(
        review_job_runner,
        "review_game",
        fake_review_game,
    )

    result = review_job_runner.run_review_job(
        job_id=uuid4(),
        pgn="test-pgn",
        depth=17,
    )

    assert result == '{"reviewed_moves":[]}'
    assert rq_job.meta == {
        "completed_plies": 12,
        "total_plies": 43,
    }
    assert rq_job.save_meta.call_count == 2

    reviewed_game.model_dump_json.assert_called_once_with()

def test_run_review_job_saves_error_and_reraises(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rq_job = MagicMock()
    rq_job.meta = {}

    def failing_review_game(
        pgn: str,
        depth: int,
        progress_callback,
    ):
        raise RuntimeError(
            "Stockfish unexpectedly stopped"
        )

    monkeypatch.setattr(
        review_job_runner,
        "get_current_job",
        lambda: rq_job,
    )
    monkeypatch.setattr(
        review_job_runner,
        "review_game",
        failing_review_game,
    )

    with pytest.raises(
        RuntimeError,
        match="Stockfish unexpectedly stopped",
    ):
        review_job_runner.run_review_job(
            job_id=uuid4(),
            pgn="test-pgn",
            depth=17,
        )

    assert rq_job.meta["error"] == (
        "Stockfish unexpectedly stopped"
    )
    rq_job.save_meta.assert_called_once_with()

def test_run_review_job_requires_rq_worker_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        review_job_runner,
        "get_current_job",
        lambda: None,
    )

    with pytest.raises(
        RuntimeError,
        match="must execute inside an RQ worker",
    ):
        review_job_runner.run_review_job(
            job_id=uuid4(),
            pgn="test-pgn",
            depth=17,
        )

@pytest.mark.parametrize(
    ("rq_status", "expected_status"),
    [
        (
            JobStatus.QUEUED,
            ReviewJobStatus.QUEUED,
        ),
        (
            JobStatus.SCHEDULED,
            ReviewJobStatus.QUEUED,
        ),
        (
            JobStatus.DEFERRED,
            ReviewJobStatus.QUEUED,
        ),
        (
            JobStatus.CREATED,
            ReviewJobStatus.QUEUED,
        ),
        (
            JobStatus.STARTED,
            ReviewJobStatus.RUNNING,
        ),
        (
            JobStatus.FINISHED,
            ReviewJobStatus.COMPLETED,
        ),
        (
            JobStatus.FAILED,
            ReviewJobStatus.FAILED,
        ),
        (
            JobStatus.STOPPED,
            ReviewJobStatus.FAILED,
        ),
        (
            JobStatus.CANCELED,
            ReviewJobStatus.FAILED,
        ),
    ],
)
def test_map_rq_status(
    rq_status: JobStatus,
    expected_status: ReviewJobStatus,
) -> None:
    assert (
        review_job_store.map_rq_status(rq_status)
        == expected_status
    )

def test_map_rq_status_rejects_unknown_status() -> None:
    unknown_status = MagicMock()

    with pytest.raises(
        ValueError,
        match="Unknown RQ job status",
    ):
        review_job_store.map_rq_status(
            unknown_status
        )

def test_enqueue_review_job_creates_rq_job(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixed_job_id = UUID(
        "11111111-1111-1111-1111-111111111111"
    )

    enqueue_mock = MagicMock()

    monkeypatch.setattr(
        review_job_store,
        "uuid4",
        lambda: fixed_job_id,
    )
    monkeypatch.setattr(
        review_job_store.review_queue,
        "enqueue",
        enqueue_mock,
    )

    response = review_job_store.enqueue_review_job(
        pgn="test-pgn",
        depth=17,
    )

    assert response.job_id == fixed_job_id
    assert (
        response.status
        == ReviewJobStatus.QUEUED
    )

    enqueue_mock.assert_called_once_with(
        review_job_store.run_review_job,
        fixed_job_id,
        "test-pgn",
        17,
        job_id=str(fixed_job_id),
        job_timeout=(
            review_job_store.JOB_TIMEOUT
        ),
        result_ttl=(
            review_job_store.JOB_RESULT_TTL
        ),
        failure_ttl=(
            review_job_store.JOB_FAILURE_TTL
        ),
        meta={
            "completed_plies": 0,
            "total_plies": None,
            "error": None,
        },
    )

def test_get_review_job_returns_none_when_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fetch_mock = MagicMock(
        side_effect=review_job_store.NoSuchJobError(
            "missing job"
        )
    )

    monkeypatch.setattr(
        review_job_store.Job,
        "fetch",
        fetch_mock,
    )

    job_id = uuid4()

    result = review_job_store.get_review_job(
        job_id
    )

    assert result is None

    fetch_mock.assert_called_once_with(
        str(job_id),
        connection=review_job_store.redis_client,
    )

@pytest.mark.parametrize(
    ("rq_status", "expected_status"),
    [
        (
            JobStatus.QUEUED,
            ReviewJobStatus.QUEUED,
        ),
        (
            JobStatus.STARTED,
            ReviewJobStatus.RUNNING,
        ),
    ],
)
def test_get_review_job_maps_active_job(
    monkeypatch: pytest.MonkeyPatch,
    rq_status: JobStatus,
    expected_status: ReviewJobStatus,
) -> None:
    rq_job = MagicMock()
    rq_job.get_status.return_value = rq_status
    rq_job.get_meta.return_value = {
        "completed_plies": 12,
        "total_plies": 43,
        "error": None,
    }

    monkeypatch.setattr(
        review_job_store.Job,
        "fetch",
        MagicMock(return_value=rq_job),
    )

    job_id = uuid4()

    result = review_job_store.get_review_job(
        job_id
    )

    assert result is not None
    assert result.job_id == job_id
    assert result.status == expected_status
    assert result.completed_plies == 12
    assert result.total_plies == 43
    assert result.result is None
    assert result.error is None

    rq_job.get_status.assert_called_once_with(
        refresh=True
    )
    rq_job.get_meta.assert_called_once_with(
        refresh=True
    )
    rq_job.return_value.assert_not_called()

def test_get_review_job_returns_completed_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    job_id = uuid4()
    raw_result = '{"reviewed_moves":[]}'

    rq_job = MagicMock()
    rq_job.get_status.return_value = (
        JobStatus.FINISHED
    )
    rq_job.get_meta.return_value = {
        "completed_plies": 43,
        "total_plies": 43,
        "error": None,
    }
    rq_job.return_value.return_value = raw_result

    validated_result = MagicMock()

    validate_mock = MagicMock(
        return_value=validated_result
    )

    review_job_constructor = MagicMock()
    expected_review_job = MagicMock()
    review_job_constructor.return_value = (
        expected_review_job
    )

    monkeypatch.setattr(
        review_job_store.Job,
        "fetch",
        MagicMock(return_value=rq_job),
    )
    monkeypatch.setattr(
        review_job_store.GameReviewResponse,
        "model_validate_json",
        validate_mock,
    )
    monkeypatch.setattr(
        review_job_store,
        "ReviewJob",
        review_job_constructor,
    )

    result = review_job_store.get_review_job(
        job_id
    )

    assert result is expected_review_job

    validate_mock.assert_called_once_with(
        raw_result
    )

    review_job_constructor.assert_called_once_with(
        job_id=job_id,
        status=ReviewJobStatus.COMPLETED,
        completed_plies=43,
        total_plies=43,
        result=validated_result,
        error=None,
    )

def test_get_review_job_returns_failure_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rq_job = MagicMock()
    rq_job.get_status.return_value = (
        JobStatus.FAILED
    )
    rq_job.get_meta.return_value = {
        "completed_plies": 8,
        "total_plies": 43,
        "error": "Stockfish crashed",
    }

    monkeypatch.setattr(
        review_job_store.Job,
        "fetch",
        MagicMock(return_value=rq_job),
    )

    job_id = uuid4()

    result = review_job_store.get_review_job(
        job_id
    )

    assert result is not None
    assert result.status == ReviewJobStatus.FAILED
    assert result.completed_plies == 8
    assert result.total_plies == 43
    assert result.result is None
    assert result.error == "Stockfish crashed"

def test_get_review_job_uses_default_failure_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rq_job = MagicMock()
    rq_job.get_status.return_value = (
        JobStatus.FAILED
    )
    rq_job.get_meta.return_value = {
        "completed_plies": 0,
        "total_plies": None,
        "error": None,
    }

    monkeypatch.setattr(
        review_job_store.Job,
        "fetch",
        MagicMock(return_value=rq_job),
    )

    result = review_job_store.get_review_job(
        uuid4()
    )

    assert result is not None
    assert result.error == "Game review failed"