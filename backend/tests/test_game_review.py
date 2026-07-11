import chess
import pytest

from app.schemas.analysis import AnalysisResponse
from app.services import engine as engine_service
from app.services import game_review as game_review_service

SHORT_PGN = """
[Event "Regression Test"]
[Site "Local"]
[Date "2026.07.11"]
[Round "?"]
[White "White Player"]
[Black "Black Player"]
[Result "*"]
[WhiteElo "1500"]
[BlackElo "1450"]

1. e4 e5 2. Nf3 Nc6 *
"""

EMPTY_PGN = """
[Event "Empty Game"]
[Site "Local"]
[Date "2026.07.11"]
[Round "?"]
[White "White Player"]
[Black "Black Player"]
[Result "*"]

*
"""

class FakeEngine:
    def __init__(self):
        self.quit_called = False

    def quit(self):
        self.quit_called = True


def create_fake_analysis(
    board: chess.Board,
    evaluation_cp: int,
) -> AnalysisResponse:
    return AnalysisResponse(
        fen=board.fen(),
        best_move_uci=None,
        best_move_san=None,
        evaluation_cp=evaluation_cp,
        mate_in=None,
        main_variation=[],
    )


def test_review_game_reviews_every_move_and_reuses_analyses(
    monkeypatch,
):
    fake_engine = FakeEngine()
    start_calls = []
    analyzed_fens = []

    evaluations = iter([10, 20, 30, 40, 50])

    def fake_start_stockfish():
        start_calls.append(True)
        return fake_engine

    def fake_analyze_board(board, engine, depth):
        assert engine is fake_engine
        assert depth == 8

        analyzed_fens.append(board.fen())

        return create_fake_analysis(
            board,
            next(evaluations),
        )

    monkeypatch.setattr(
        game_review_service,
        "start_stockfish",
        fake_start_stockfish,
    )

    monkeypatch.setattr(
        game_review_service,
        "analyze_board",
        fake_analyze_board,
    )

    result = game_review_service.review_game(
        SHORT_PGN,
        depth=8,
    )

    assert result.white == "White Player"
    assert result.black == "Black Player"
    assert result.white_elo == 1500
    assert result.black_elo == 1450
    assert result.result == "*"

    assert len(result.reviewed_moves) == 4

    assert len(analyzed_fens) == 5

    assert len(start_calls) == 1

    assert result.reviewed_moves[0].move_uci == "e2e4"
    assert result.reviewed_moves[-1].move_uci == "b8c6"

    assert [
        move.color
        for move in result.reviewed_moves
    ] == [
        "white",
        "black",
        "white",
        "black",
    ]


    for index in range(len(result.reviewed_moves) - 1):
        current_move = result.reviewed_moves[index]
        next_move = result.reviewed_moves[index + 1]

        assert current_move.fen_after == next_move.fen_before

        assert (
            current_move.eval_cp_after
            == next_move.eval_cp_before
        )

    assert fake_engine.quit_called is True


def test_review_game_with_no_moves_does_not_start_stockfish(
    monkeypatch,
):
    def fail_if_stockfish_starts():
        pytest.fail(
            "Stockfish should not start for a game with no moves"
        )

    monkeypatch.setattr(
        game_review_service,
        "start_stockfish",
        fail_if_stockfish_starts,
    )

    result = game_review_service.review_game(
        EMPTY_PGN,
        depth=8,
    )

    assert result.white == "White Player"
    assert result.black == "Black Player"
    assert result.reviewed_moves == []


def test_review_game_closes_stockfish_when_analysis_fails(
    monkeypatch,
):
    fake_engine = FakeEngine()

    def fake_start_stockfish():
        return fake_engine

    def failing_analyze_board(board, engine, depth):
        raise RuntimeError("Engine analysis failed")

    monkeypatch.setattr(
        game_review_service,
        "start_stockfish",
        fake_start_stockfish,
    )

    monkeypatch.setattr(
        game_review_service,
        "analyze_board",
        failing_analyze_board,
    )

    with pytest.raises(
        RuntimeError,
        match="Engine analysis failed",
    ):
        game_review_service.review_game(
            SHORT_PGN,
            depth=8,
        )

    assert fake_engine.quit_called is True


def test_review_move_uses_one_engine_for_both_positions(
    monkeypatch,
):
    fake_engine = FakeEngine()
    start_calls = []
    analyzed_fens = []

    evaluations = iter([10, 20])

    def fake_start_stockfish():
        start_calls.append(True)
        return fake_engine

    def fake_analyze_board(board, engine, depth):
        assert engine is fake_engine
        assert depth == 8

        analyzed_fens.append(board.fen())

        return create_fake_analysis(
            board,
            next(evaluations),
        )

    monkeypatch.setattr(
        engine_service,
        "start_stockfish",
        fake_start_stockfish,
    )

    monkeypatch.setattr(
        engine_service,
        "analyze_board",
        fake_analyze_board,
    )

    result = engine_service.review_move(
        fen_before=chess.STARTING_FEN,
        move_uci="e2e4",
        depth=8,
    )

    assert len(start_calls) == 1
    assert len(analyzed_fens) == 2

    assert result.move_uci == "e2e4"
    assert result.move_san == "e4"
    assert result.fen_before == chess.STARTING_FEN
    assert result.eval_cp_before == 10
    assert result.eval_cp_after == 20
    assert result.move_accuracy == 100

    assert fake_engine.quit_called is True