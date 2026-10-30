import httpx
from app.core.config import LICHESS_API_TOKEN

LICHESS_EXPLORER_BASE_URL = "https://explorer.lichess.org"
MIN_BOOK_FREQUENCY = 0.01
MIN_BOOK_GAMES = 20


def create_client():
  return httpx.Client(
    base_url=LICHESS_EXPLORER_BASE_URL,
    headers={
        "Authorization": f"Bearer {LICHESS_API_TOKEN}",
        "User-Agent": "ChessCoach",
    },
    timeout=10,
)

def is_book_move(client: httpx.Client, fen_before: str, move_uci: str) -> bool:
  response = client.get(
      "/lichess",
      params={
          "variant": "standard",
          "fen": fen_before,
          "speeds": "classical",
          "ratings": "2200,2500",
          "moves": 50,
      },
  )

  response.raise_for_status()

  data = response.json()

  position_games = data.get("white", 0) + data.get("draws", 0) + data.get("black", 0)
  move_games = 0

  for move_entry in data["moves"]:
      if move_entry["uci"] == move_uci:
        move_games = move_entry.get("white", 0) + move_entry.get("draws", 0) + move_entry.get("black", 0)
        break

  move_frequency = move_games / position_games if position_games > 0 else 0

  return (move_frequency >= MIN_BOOK_FREQUENCY and move_games >= MIN_BOOK_GAMES)    



