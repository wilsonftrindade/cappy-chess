from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.game import Game
from app.models.review import Review
from app.schemas.review_job import ReviewJobStatus
from app.schemas.game import ParsedGameResponse
from app.services.pgn_parser import parse_pgn, compute_game_hash

def get_or_create_game_and_review(session: Session, pgn: str, depth: int) -> tuple[Review, bool]:
  parsed_game = parse_pgn(pgn)
  game_hash = compute_game_hash(pgn)

  game = session.scalar(select(Game).where(Game.game_hash == game_hash))

  if game is None:
    game = Game(
      pgn=pgn,
      white_name=parsed_game.white,
      black_name=parsed_game.black,
      white_elo=parsed_game.white_elo,
      black_elo=parsed_game.black_elo,
      result=parsed_game.result,
      game_hash=game_hash,
    )

    session.add(game)
    session.flush()

  review = session.scalar(select(Review).where(Review.game_id == game.id, Review.depth == depth))
  if review is not None:
    return review, False

  review = Review(
    game_id=game.id,
    depth=depth,
    status=ReviewJobStatus.QUEUED,
  )

  session.add(review)
  session.commit()

  return review, True