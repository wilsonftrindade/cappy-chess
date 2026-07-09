import chess
import chess.engine
from fastapi import HTTPException
from app.schemas.analysis import AnalysisResponse, MoveReviewResponse
import os, math
from dotenv import load_dotenv
from .classification import *

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

    try:
        board_before = chess.Board(fen_before)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid FEN before the move")
    
    analysis_before = analyze_fen(fen_before, depth)
    eval_cp_before = analysis_before.evaluation_cp
    mate_in_before = analysis_before.mate_in
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

    move_san = board_before.san(move)

    fen_after = board_after.fen()
    analysis_after = analyze_fen(fen_after, depth)
    eval_cp_after = analysis_after.evaluation_cp
    mate_in_after = analysis_after.mate_in

    is_white = board_before.turn == chess.WHITE
    
    eval_cp_loss = compute_eval_cp_loss(eval_cp_before, eval_cp_after, is_white)
    win_probability_before = player_win_probability(eval_cp_before, mate_in_before, is_white)
    win_probability_after = player_win_probability(eval_cp_after, mate_in_after, is_white)
    win_probability_loss = compute_win_probability_loss(win_probability_before, win_probability_after)

    classification = classify_move(move_uci, best_move_uci, win_probability_loss, mate_in_before, mate_in_after, is_white)
    
    return MoveReviewResponse(
        fen_before=fen_before,
        move_uci=move_uci,
        move_san=move_san,
        best_move_uci=best_move_uci,
        best_move_san=best_move_san,
        eval_cp_before=eval_cp_before,
        eval_cp_after=eval_cp_after,
        eval_cp_loss=eval_cp_loss,
        mate_in_before=mate_in_before,
        mate_in_after=mate_in_after,
        win_probability_before=win_probability_before,
        win_probability_after=win_probability_after,
        win_probability_loss=win_probability_loss,
        classification=classification
    )






