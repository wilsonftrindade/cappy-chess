import pytest

from app.services.classification import (
    compute_win_probability_loss,
    compute_eval_cp_loss,
    cp_to_win_probability,
    mate_for_player,
    player_win_probability,
    classify_move_by_expected_points_loss,
    classify_mate_scenario,
    classify_move,
)


def test_compute_win_probability_loss_normal_loss():
    assert compute_win_probability_loss(0.70, 0.55) == pytest.approx(0.15)


def test_compute_win_probability_loss_never_negative():
    assert compute_win_probability_loss(0.55, 0.70) == 0


def test_compute_win_probability_loss_returns_none_if_missing():
    assert compute_win_probability_loss(None, 0.70) is None
    assert compute_win_probability_loss(0.70, None) is None


def test_compute_eval_cp_loss_for_white():
    assert compute_eval_cp_loss(100, -50, True) == 150


def test_compute_eval_cp_loss_for_black():
    assert compute_eval_cp_loss(-100, 50, False) == 150


def test_compute_eval_cp_loss_never_negative_for_white():
    assert compute_eval_cp_loss(50, 100, True) == 0


def test_cp_to_win_probability_equal_position_is_around_half():
    assert cp_to_win_probability(0) == pytest.approx(0.5)


def test_cp_to_win_probability_positive_eval_above_half():
    assert cp_to_win_probability(300) > 0.5


def test_cp_to_win_probability_negative_eval_below_half():
    assert cp_to_win_probability(-300) < 0.5


def test_mate_for_player_white_perspective():
    assert mate_for_player(3, True) == 3
    assert mate_for_player(-3, True) == -3


def test_mate_for_player_black_perspective():
    assert mate_for_player(3, False) == -3
    assert mate_for_player(-3, False) == 3


def test_player_win_probability_when_player_is_mating():
    assert player_win_probability(None, 3, True) == 1.0


def test_player_win_probability_when_player_is_getting_mated():
    assert player_win_probability(None, -3, True) == 0.0


def test_player_win_probability_for_black_flips_white_probability():
    white_probability = cp_to_win_probability(200)
    black_probability = player_win_probability(200, None, False)

    assert black_probability == pytest.approx(1 - white_probability)


def test_classify_best_when_played_move_equals_best_move():
    result = classify_move_by_expected_points_loss(
        win_probability_loss=0.15,
        played_move_uci="e2e4",
        best_move_uci="e2e4",
    )

    assert result == "Best"


def test_classify_expected_points_loss_best():
    result = classify_move_by_expected_points_loss(
        win_probability_loss=0.001,
        played_move_uci="d2d4",
        best_move_uci="e2e4",
    )

    assert result == "Best"


def test_classify_expected_points_loss_excellent():
    result = classify_move_by_expected_points_loss(
        win_probability_loss=0.01,
        played_move_uci="d2d4",
        best_move_uci="e2e4",
    )

    assert result == "Excellent"


def test_classify_expected_points_loss_good():
    result = classify_move_by_expected_points_loss(
        win_probability_loss=0.03,
        played_move_uci="d2d4",
        best_move_uci="e2e4",
    )

    assert result == "Good"


def test_classify_expected_points_loss_inaccuracy():
    result = classify_move_by_expected_points_loss(
        win_probability_loss=0.07,
        played_move_uci="d2d4",
        best_move_uci="e2e4",
    )

    assert result == "Inaccuracy"


def test_classify_expected_points_loss_mistake():
    result = classify_move_by_expected_points_loss(
        win_probability_loss=0.15,
        played_move_uci="d2d4",
        best_move_uci="e2e4",
    )

    assert result == "Mistake"


def test_classify_expected_points_loss_blunder():
    result = classify_move_by_expected_points_loss(
        win_probability_loss=0.30,
        played_move_uci="d2d4",
        best_move_uci="e2e4",
    )

    assert result == "Blunder"


def test_mate_scenario_player_finds_forced_mate():
    result = classify_mate_scenario(
        mate_in_before=None,
        mate_in_after=3,
        is_white=True,
        played_move_uci="h5f7",
        best_move_uci="h5e8",
    )

    assert result == "Excellent"


def test_mate_scenario_player_keeps_forced_mate_with_best_move():
    result = classify_mate_scenario(
        mate_in_before=3,
        mate_in_after=2,
        is_white=True,
        played_move_uci="h5f7",
        best_move_uci="h5f7",
    )

    assert result == "Best"


def test_mate_scenario_player_keeps_forced_mate_not_best():
    result = classify_mate_scenario(
        mate_in_before=3,
        mate_in_after=5,
        is_white=True,
        played_move_uci="h5f7",
        best_move_uci="h5e8",
    )

    assert result == "Excellent"


def test_mate_scenario_player_loses_forced_mate_falls_back_to_expected_points():
    result = classify_mate_scenario(
        mate_in_before=3,
        mate_in_after=None,
        is_white=True,
        played_move_uci="h5f7",
        best_move_uci="h5e8",
    )

    assert result is None


def test_mate_scenario_player_allows_forced_mate_falls_back_to_expected_points():
    result = classify_mate_scenario(
        mate_in_before=None,
        mate_in_after=-4,
        is_white=True,
        played_move_uci="a2a3",
        best_move_uci="g2g3",
    )

    assert result is None


def test_mate_scenario_player_escapes_detected_mate():
    result = classify_mate_scenario(
        mate_in_before=-3,
        mate_in_after=None,
        is_white=True,
        played_move_uci="g2g3",
        best_move_uci="h2h3",
    )

    assert result == "Excellent"


def test_classify_move_falls_back_to_expected_points_loss():
    result = classify_move(
        played_move_uci="f2f3",
        best_move_uci="e2e4",
        win_probability_loss=0.25,
        mate_in_before=None,
        mate_in_after=None,
        is_white=True,
    )

    assert result == "Blunder"