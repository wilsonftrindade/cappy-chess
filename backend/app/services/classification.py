import math

def compute_win_probability_loss(before: float | None, after: float | None) -> float | None:
    if before is None or after is None:
        return None
    
    else:
        return max(0, before - after)

def compute_eval_cp_loss(before: int | None, after: int | None, is_white: bool) -> int | None:
    if before is None or after is None:
        return None
    
    if is_white:
        return max(0, before - after)
    else:
        # eval_cp is from white's pov, so compute its negative for black
        return max(0, after - before)


def cp_to_win_probability(cp: int) -> float:
    # translate centipawns to white's win % (centipawns are in white's perspective). Win % is returned from white's pov
    win_percent = 50 + 50 * (2 / (1 + math.exp(-0.00368208 * cp)) - 1)
    return win_percent / 100

def mate_for_player(mate_in: int | None, is_white: bool) -> int | None:
    # normalize mate score. If negative in your turn, you are getting mated. 
    if mate_in is None:
        return None
    
    if is_white:
        return mate_in
    else:
        return -mate_in
        
def player_win_probability(eval_cp: int | None, mate_in: int | None, is_white: bool):
    # if player is getting mated, win % is 0. If player is mating, win % is 1
    if mate_in is not None:
        if mate_for_player(mate_in, is_white) < 0:
            return 0.0
        else:
            return 1.0
    
    if eval_cp is None:
        return None
    
    # if we do not have mate_in, simply convert cp to win %
    if is_white:
        return cp_to_win_probability(eval_cp)
    else:
        return 1 - cp_to_win_probability(eval_cp)
    
def classify_move_by_expected_points_loss(win_probability_loss: float, played_move_uci: str, best_move_uci: str | None) -> str:

    if best_move_uci is not None and played_move_uci == best_move_uci:
        return "Best"
    
    if win_probability_loss < 0.005:
        return "Best"
    elif win_probability_loss < 0.02:
        return "Excellent"
    elif win_probability_loss < 0.05:
        return "Good"
    elif win_probability_loss < 0.10:
        return "Inaccuracy"
    elif win_probability_loss < 0.20:
        return "Mistake"
    else:
        return "Blunder"
    
def classify_mate_scenario(mate_in_before: int | None, mate_in_after: int | None, is_white: bool, played_move_uci: str, best_move_uci: str | None) -> str | None:
    if best_move_uci is not None and played_move_uci == best_move_uci:
        return "Best"
    
    player_had_mate_before = mate_in_before is not None and mate_for_player(mate_in_before, is_white) > 0
    player_had_mate_after = mate_in_after is not None and mate_for_player(mate_in_after, is_white) > 0

    player_getting_mated_before = mate_in_before is not None and mate_for_player(mate_in_before, is_white) < 0
    player_getting_mated_after = mate_in_after is not None and mate_for_player(mate_in_after, is_white) < 0

    if not player_had_mate_before and player_had_mate_after:
        return "Excellent"
    
    if player_had_mate_before and player_had_mate_after:
        if mate_for_player(mate_in_before, is_white) > mate_for_player(mate_in_after, is_white):
            return "Best"
        else:
            return "Excellent"
        
    if player_had_mate_before and not player_had_mate_after:
        # let expected points loss handle
        return None
    
    if not player_getting_mated_before and player_getting_mated_after:
        # let expected points loss handle
        return None
    
    if player_getting_mated_before and player_getting_mated_after:
        # if gives a shorter path to mate, good; excellent if not
        before_distance = abs(mate_for_player(mate_in_before, is_white))
        after_distance = abs(mate_for_player(mate_in_after, is_white))
        if after_distance < before_distance - 1:
            return "Good"
        else:
            return "Excellent"
        
    if player_getting_mated_before and not player_getting_mated_after:
        # technically impossible, should not happen.
        return "Excellent"
    
    return None
    
def classify_move(played_move_uci: str, best_move_uci: str | None, win_probability_loss: float | None, mate_in_before: int | None, mate_in_after: int | None, is_white: bool) -> str | None:
    if played_move_uci == best_move_uci:
        return "Best"
    
    mate_classification = classify_mate_scenario(mate_in_before, mate_in_after, is_white, played_move_uci, best_move_uci)

    if mate_classification is not None:
        return mate_classification
    
    if win_probability_loss is None:
        return None
    
    return classify_move_by_expected_points_loss(win_probability_loss, played_move_uci, best_move_uci)

    
    

    
    
     
