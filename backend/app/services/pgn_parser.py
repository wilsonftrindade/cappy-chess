import chess.pgn
import io
from fastapi import HTTPException
from app.schemas.game import ParsedGameResponse, ParsedMove

def parse_elo(elo: str | None)-> int | None:
    try:
        return int(elo)
    except (ValueError, TypeError):
        return None
    

def parse_pgn(pgn_text: str) -> ParsedGameResponse:

    if not pgn_text.strip():
        raise HTTPException(status_code=400, detail="PGN cannot be empty")

    pgn_io = io.StringIO(pgn_text)
    game = chess.pgn.read_game(pgn_io)

    if game is None:
        raise HTTPException(status_code=400, detail="Invalid PGN format")
    
    board = game.board()
    moves: list[ParsedMove] = []

    for index, move in enumerate(game.mainline_moves()):
        fen_before = board.fen()
        san = board.san(move)
        uci = move.uci()

        board.push(move)
        fen_after = board.fen()
        move_number = index // 2 + 1
        color = "white" if index % 2 == 0 else "black"
        parsed_move = ParsedMove(
            move_number=move_number,
            color=color,
            move_san=san,
            move_uci=uci,
            fen_before=fen_before,
            fen_after=fen_after
        )
        moves.append(parsed_move)
    
    result = game.headers.get("Result")
    white = game.headers.get("White")
    black = game.headers.get("Black")
    white_elo = parse_elo(game.headers.get("WhiteElo"))
    black_elo = parse_elo(game.headers.get("BlackElo"))

    return ParsedGameResponse(
        white=white,
        black=black,
        result=result,
        white_elo=white_elo,
        black_elo=black_elo,
        moves=moves
    )