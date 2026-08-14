import httpx
import json
from datetime import datetime, timezone

from app.schemas.imports import ImportedGame

LICHESS_BASE_URL = "https://lichess.org/api"
LICHESS_HEADERS = {"Accept": "application/x-ndjson", "User-Agent": "wilsonferreiratrindadeneto2028@u.northwestern.edu"}

async def fetch_lichess_games(username: str, limit: int = 20) -> list[dict]:
  async with httpx.AsyncClient(
    base_url=LICHESS_BASE_URL, headers=LICHESS_HEADERS, timeout=15
    ) as client:
    response = await client.get(f"/games/user/{username}?max={limit}&pgnInJson=true")
    response.raise_for_status()
    data = [json.loads(line) for line in response.text.splitlines() if line.strip()]
    return data

def transform_lichess_game(game: dict) -> ImportedGame:
  if game.get("winner") == "white":
    result = "1-0"
  elif game.get("winner") == "black":
    result = "0-1"
  else:
    result = "1/2-1/2"

  return ImportedGame(
    pgn=game["pgn"],
    source="lichess",
    external_id=game["id"],
    white=game["players"]["white"]["user"]["name"],
    black=game["players"]["black"]["user"]["name"],
    white_elo=game["players"]["white"].get("rating"),
    black_elo=game["players"]["black"].get("rating"),
    result=result,
    played_at=datetime.fromtimestamp(game["createdAt"] / 1000, tz=timezone.utc),
    time_class=game["speed"]
  )
