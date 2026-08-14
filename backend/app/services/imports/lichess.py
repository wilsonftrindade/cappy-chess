import httpx
import json
from datetime import datetime, timezone

from app.schemas.imports import ImportedGame

LICHESS_BASE_URL = "https://lichess.org/api"
LICHESS_HEADERS = {"Accept": "application/x-ndjson", "User-Agent": "wilsonferreiratrindadeneto2028@u.northwestern.edu"}

async def fetch_lichess_games(username: str, limit: int = 20, cursor: str | None = None) -> tuple[list[dict], str | None]:

  params = {"max": limit + 1, "pgnInJson": True}

  if cursor is not None:
    params["until"] = int(cursor)
          
  async with httpx.AsyncClient(
    base_url=LICHESS_BASE_URL, headers=LICHESS_HEADERS, timeout=15
    ) as client:
    response = await client.get(f"/games/user/{username}", params=params)
    response.raise_for_status()
    data = [json.loads(line) for line in response.text.splitlines() if line.strip()]

    new_cursor = None
    if len(data) > limit:
      new_cursor = data[-1]["createdAt"] + 1
      print(new_cursor)

    return data[:limit], str(new_cursor)

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
