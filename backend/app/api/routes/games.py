from app.schemas.game import ParsedGameResponse, ParseGameRequest
from app.services.pgn_parser import parse_pgn
from fastapi import APIRouter

router = APIRouter()

@router.post("/parse", response_model=ParsedGameResponse)
def parse_game(pgn_request: ParseGameRequest):
    return parse_pgn(pgn_request.pgn)
