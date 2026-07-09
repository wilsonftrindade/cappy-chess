import chess
import chess.engine
from fastapi import HTTPException
from app.schemas.analysis import AnalysisResponse, MoveReviewResponse
import os, math
from dotenv import load_dotenv

load_dotenv()

STOCKFISH_PATH = os.getenv("STOCKFISH_PATH", "stockfish")

def analyze_fen(fen: str, depth: int) -> AnalysisResponse:

    try:
        board = chess.Board(fen)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid FEN")
    

    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Stockfish engine not found")


    try:
        info = engine.analyse(board, chess.engine.Limit(depth=depth))

        main_variation_moves = info.get("pv", [])
        if main_variation_moves:
            best_move = main_variation_moves[0]
            best_move_san = board.san(best_move)
            best_move_uci = best_move.uci()
        else:
            best_move = None
            best_move_san = None
            best_move_uci = None

        evaluation = info.get("score")
        score = evaluation.white()
        evaluation_cp =  score.score()
        mate_in = score.mate()
        main_variation = [move.uci() for move in main_variation_moves]

        return AnalysisResponse (
            fen=fen,
            best_move_san=best_move_san,
            best_move_uci=best_move_uci,
            evaluation_cp=evaluation_cp,
            mate_in=mate_in,
            main_variation=main_variation
            )
        
    finally:
        engine.quit()



def review_move(fen_before: str, move_uci: str, depth: int) -> MoveReviewResponse:
    # Still need to handle mate scores

    try:
        board_before = chess.Board(fen_before)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid FEN before the move")
    
    analysis_before = analyze_fen(fen_before, depth)
    eval_cp_before = analysis_before.evaluation_cp
    best_move_uci = analysis_before.best_move_uci
    best_move_san = analysis_before.best_move_san

    try:
        move = chess.Move.from_uci(move_uci)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UCI move")

    board_after = board_before.copy()

    if move not in board_before.legal_moves:
        raise HTTPException(status_code=400, detail="Illegal move")
    
    board_after.push(move)

    fen_after = board_after.fen()
    analysis_after = analyze_fen(fen_after, depth)
    eval_cp_after = analysis_after.evaluation_cp

    if board_before.turn == chess.WHITE:
        eval_cp_loss = eval_cp_before - eval_cp_after
    else:
        eval_cp_loss = eval_cp_after - eval_cp_before

    win_probability_before = color_win_probability(eval_cp_before, board_before.turn == chess.WHITE)
    win_probability_after = color_win_probability(eval_cp_after, board_before.turn == chess.WHITE)
    
    win_probability_loss = win_probability_before - win_probability_after

    if move_uci == best_move_uci:
        classification = "Best"
    else:
        classification = classify_move(win_probability_loss)

    move_san = board_before.san(move)

    return MoveReviewResponse(
        fen_before=fen_before,
        move_uci=move_uci,
        move_san=move_san,
        best_move_uci=best_move_uci,
        best_move_san=best_move_san,
        eval_cp_before=eval_cp_before,
        eval_cp_after=eval_cp_after,
        eval_cp_loss=eval_cp_loss,
        win_probability_before=win_probability_before,
        win_probability_after=win_probability_after,
        win_probability_loss=win_probability_loss,
        classification=classification
    )


def classify_move(win_percentage_loss: int) -> str:

    win_percentage_loss = max(0, win_percentage_loss)
    
    if win_percentage_loss < 0.005:
        return "Best"
    elif win_percentage_loss < 0.02:
        return "Excellent"
    elif win_percentage_loss < 0.05:
        return "Good"
    elif win_percentage_loss < 0.10:
        return "Inaccuracy"
    elif win_percentage_loss < 0.20:
        return "Mistake"
    elif win_percentage_loss < 1:
        return "Blunder"

def cp_to_win_probability(cp: int) -> float:
    # translate centipawns to white's win % (centipawns are in white's perspective)
    win_percent = 50 + 50 * (2 / (1 + math.exp(-0.00368208 * cp)) - 1)
    return win_percent / 100

def color_win_probability(cp: int, is_white: bool):
    if is_white:
        return cp_to_win_probability(cp)
    else:
        return 1 - cp_to_win_probability(cp)
    

        

    


