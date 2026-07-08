import chess
import chess.engine
from fastapi import HTTPException
from app.schemas.analysis import AnalysisResponse, MoveReviewResponse
import os
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

    classification = classify_move(eval_cp_loss)
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
        classification=classification
    )


def classify_move(eval_cp_loss: int) -> str:

    eval_cp_loss = max(0, eval_cp_loss)
    
    if eval_cp_loss < 20:
        return "Excellent"
    elif eval_cp_loss < 70:
        return "Good"
    elif eval_cp_loss < 150:
        return "Inaccuracy"
    elif eval_cp_loss < 300:
        return "Mistake"
    else:
        return "Blunder"


        

    


