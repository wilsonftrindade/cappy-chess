import chess
import chess.engine
from fastapi import HTTPException
from app.schemas.analysis import AnalysisResponse
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




        

    


