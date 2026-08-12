import chess.pgn
from hashlib import sha256
import io
from fastapi import HTTPException
from app.schemas.game import ParsedGameResponse, ParsedMove

def parse_elo(elo: str | None)-> int | None:
    try:
        return int(elo)
    except (ValueError, TypeError):
        return None

def compute_game_hash(pgn: str) -> str:
    game = chess.pgn.read_game(io.StringIO(pgn))

    if game is None:
        raise ValueError("Invalid PGN")

    id_headers = ("Event", "Site", "Date", "Round", "White", "Black", "Result", "FEN")
    normalized_headers = "|".join(game.headers.get(header, "") for header in id_headers)

    normalized_moves = " ".join(move.uci() for move in game.mainline_moves())

    canonical_game = (f"{normalized_headers}|{normalized_moves}")
    game_hash = sha256(canonical_game.encode()).hexdigest()
    return game_hash


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
