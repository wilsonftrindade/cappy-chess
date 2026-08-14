import httpx
from datetime import datetime, timezone

from app.schemas.imports import ImportedGame

CHESS_COM_BASE_URL = "https://api.chess.com/pub"
CHESS_COM_HEADERS = {"User-Agent": "ChessCoach/1.0"}

async def fetch_chess_com_games(username: str, limit: int = 20, cursor: str | None = None) -> tuple[list[dict], str | None]:

  async with httpx.AsyncClient(
      base_url=CHESS_COM_BASE_URL, headers=CHESS_COM_HEADERS, timeout=15
  ) as client:
    
    response = await client.get(f"/player/{username}/games/archives")
    response.raise_for_status()
    data = response.json()

    archives = data.get("archives", [])
    archives.reverse() # reverse into descending order

    games = []
    before = int(cursor) if cursor is not None else None
    new_cursor = None

    for archive_url in archives:
      archive_response = await client.get(archive_url)
      archive_response.raise_for_status()
      archive_data = archive_response.json()

      archive_games = archive_data.get("games", [])
      archive_games.reverse() # reverse into descending order

      eligible_games = [game for game in archive_games if before is None or game["end_time"] < before]

      games.extend(eligible_games)

      if len(games) >= limit + 1:
        break

    if len(games) > limit:
      new_cursor = games[limit - 1]["end_time"]

    return games[:limit], str(new_cursor)


def transform_chess_com_game(game: dict) -> ImportedGame:

  if game["white"]["result"] == "win":
    result = "1-0"
  elif game["black"]["result"] == "win":
    result = "0-1"
  else:
    result = "1/2-1/2"
  
  return ImportedGame(
    pgn=game["pgn"],
    source="chess_com",
    external_id=game["url"],
    white=game["white"]["username"],
    black=game["black"]["username"],
    white_elo=game["white"].get("rating"),
    black_elo=game["black"].get("rating"),
    result=result,
    played_at=datetime.fromtimestamp(game["end_time"], tz=timezone.utc),
    time_class=game["time_class"]
  )
      

  




      


