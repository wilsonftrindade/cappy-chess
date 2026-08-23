from app.schemas.analysis import PlayerReviewSummary, ReviewedMove
from .classification import player_win_probability
from statistics import pstdev

def build_player_summary(reviewed_moves: list[ReviewedMove], color: str) -> PlayerReviewSummary:
    player_moves = []
    for reviewed_move in reviewed_moves:
        if reviewed_move.color == color:
            player_moves.append(reviewed_move)

    move_count = len(player_moves)
    accuracy = compute_player_accuracy(reviewed_moves, color)
    classification_counts = count_player_classsifications(player_moves)
    return PlayerReviewSummary(
        move_count=move_count,
        accuracy=accuracy,
        classification_counts=classification_counts
    )

def compute_player_accuracy(reviewed_moves: list[ReviewedMove], color: str) -> float:
    if not reviewed_moves:
        return None
    
    player_moves = [move for move in reviewed_moves if move.color == color]

    if any(move.move_accuracy is None for move in player_moves):
        raise ValueError(f"Missing move accuracy for {color}")
    
    first_move = reviewed_moves[0]

    initial_white_win_probability = player_win_probability(first_move.eval_cp_before, first_move.mate_in_before, is_white=True,)

    if initial_white_win_probability is None:
        raise ValueError("Initial position has no usable evaluation")

    white_win_probabilities = [initial_white_win_probability]

    for move in reviewed_moves:
        win_probability_after = player_win_probability(move.eval_cp_after, move.mate_in_after, is_white=True)
        white_win_probabilities.append(win_probability_after)

    if any(probability is None for probability in white_win_probabilities):
        raise ValueError(f"Missing win probability for {color}")

    weights = calculate_volatility_weights(white_win_probabilities, len(reviewed_moves))
    accuracy_and_weights = []

    for move, weight in zip(reviewed_moves, weights):
        accuracy_and_weight = (
            move.move_accuracy,
            weight,
        )

        if move.color == color:
            accuracy_and_weights.append(accuracy_and_weight)

    mistake_accuracy = power_loss_accuracy(accuracy_and_weights, 2)

    base_accuracy = weighted_mean([(move.move_accuracy, severity_weight(move.move_accuracy)) for move in player_moves])

    final_accuracy = 0.5 * base_accuracy + 0.5 * mistake_accuracy

    return final_accuracy

def calculate_volatility_weights(win_probabilities: list[float], number_of_plies: int) -> list[float]:

    if number_of_plies == 0:
        return []
    
    win_percentages = [win_probability * 100 for win_probability in win_probabilities]

    window_size = compute_window_size(number_of_plies)

    first_window = win_percentages[:window_size]

    # so that # of windows matches the # of moves
    windows = [first_window for _ in range(window_size - 2)]

    for start in range(len(win_percentages) - window_size + 1):
        window = win_percentages[start : start + window_size]
        windows.append(window)

    weights = []

    # for window in windows:
    #     volatility = pstdev(window)
    #     weight = max(0.5, min(volatility, 12)) 
    #     weights.append(weight)

    for window in windows:
        volatility = pstdev(window)
        normalized_vol = min(volatility, 12) /12
        weight = 1 + 0.5 * normalized_vol
        weights.append(weight)
    
    return weights

def compute_window_size(number_of_plies: int) -> int:
    return max(2, min(number_of_plies // 10, 8))

def weighted_mean(values_and_weights: list[tuple[float, float]]) -> float | None: 
    if not values_and_weights:
        return None
    
    total_weight = sum(weight for _, weight in values_and_weights)
    weighted_sum = sum(value * weight for value, weight in values_and_weights)
    return weighted_sum / total_weight

def harmonic_mean(values: list[float]) -> float | None:
    if not values:
        return None
    
    if any(value <= 0 for value in values):
        return 0.0
    
    return len(values) / sum(1 / value for value in values)


def combine_means(values_and_weights: list[tuple[float, float]]) -> float | None:
    values = [value for value, _ in values_and_weights]

    volatility_weighted_mean = weighted_mean(values_and_weights)
    harmonic_mean_result = harmonic_mean(values)

    if (volatility_weighted_mean is None or harmonic_mean_result is None):
        return None

    game_accuracy = (volatility_weighted_mean + harmonic_mean_result) / 2

    return round(game_accuracy, 2)

    
def count_player_classsifications(player_moves: list[ReviewedMove]) -> dict[str, int]:
    classifications = ["Best", "Excellent", "Good", "Inaccuracy", "Mistake", "Blunder"]
    count = {classification: 0 for classification in classifications}

    for move in player_moves:
        count[move.classification] += 1

    return count

def power_loss_accuracy(
    values_and_weights: list[tuple[float, float]],
    power: float,
) -> float | None:
    # V2 accuracy logic, using  only a non-linear aggregate loss score
    if not values_and_weights:
        return None

    total_weight = sum(weight for _, weight in values_and_weights)

    total_power_loss = (sum(weight * ((100 - accuracy) ** power) for accuracy, weight in values_and_weights))

    mean_power_loss = total_power_loss / total_weight

    aggregate_loss = mean_power_loss ** (1 / power)

    return round(100 - aggregate_loss, 2)


def severity_weight(accuracy):
    # weights from 0.
    loss_ratio = (100 - accuracy) / 100

    severity_weight = 0.75 + 1.25 * loss_ratio ** 1.5

    return severity_weight




    