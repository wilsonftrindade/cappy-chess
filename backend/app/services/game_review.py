from app.schemas.analysis import GameReviewResponse, ReviewedMove
from .pgn_parser import parse_pgn
from .engine import start_stockfish, analyze_board, create_and_validate_board, build_move_review

def review_game(pgn: str, depth: int) -> GameReviewResponse:
    # 1. Parse the PGN.
    # 2. Start Stockfish once.
    # 3. Analyze the initial position.
    # 4. Loop through every parsed move.
    # 5. Analyze the position after that move.
    # 6. Call build_move_review().
    # 7. Add the game-specific fields to create a ReviewedMove.
    # 8. Reuse the after-analysis as the next before-analysis.
    # 9. Close Stockfish.
    # 10. Return GameReviewResponse.

    parsed_game = parse_pgn(pgn)

    reviewed_moves = []

    if not parsed_game.moves:
        return GameReviewResponse(
            white=parsed_game.white,
            black=parsed_game.black,
            result=parsed_game.result,
            white_elo=parsed_game.white_elo,
            black_elo=parsed_game.black_elo,
            reviewed_moves=reviewed_moves
        )

    fen_before = parsed_game.moves[0].fen_before
    board_before = create_and_validate_board(fen_before)

    engine = start_stockfish()

    try: 
        analysis_before = analyze_board(board_before, engine, depth)

        for parsed_move in parsed_game.moves:
            fen_after = parsed_move.fen_after
            board_after = create_and_validate_board(fen_after)
            analysis_after = analyze_board(board_after, engine, depth)

            move_uci = parsed_move.uci
            move_san = parsed_move.san
            is_white = parsed_move.color == "white"

            move_review = build_move_review(move_uci, move_san, analysis_before, analysis_after, is_white)

            reviewed_move = ReviewedMove(
                move_number=parsed_move.move_number,
                color=parsed_move.color,
                fen_after=fen_after,
                **move_review.model_dump()
            )

            reviewed_moves.append(reviewed_move)

            analysis_before = analysis_after

        return GameReviewResponse(
            white=parsed_game.white,
            black=parsed_game.black,
            result=parsed_game.result,
            white_elo=parsed_game.white_elo,
            black_elo=parsed_game.black_elo,
            reviewed_moves=reviewed_moves
        )
    finally:
        engine.quit()



