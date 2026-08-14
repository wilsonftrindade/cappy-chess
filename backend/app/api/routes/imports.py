import httpx
from fastapi import APIRouter, HTTPException, status, Query
from app.schemas.imports import ImportedGamesResponse
from app.services.imports.chess_com import fetch_chess_com_games, transform_chess_com_game

router = APIRouter()

@router.get("/chess-com/{username}/games", response_model=ImportedGamesResponse)
async def get_chess_com_games(username: str, limit: int = Query(default=20, ge=1, le=50)):
    try:
      games = await fetch_chess_com_games(username, limit)

    except httpx.HTTPStatusError as exc:
      if exc.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chess.com user not found",
            ) from exc

      if exc.response.status_code == 429:
          raise HTTPException(
              status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
              detail="Chess.com is temporarily rate limiting requests",
          ) from exc

      raise HTTPException(
          status_code=status.HTTP_502_BAD_GATEWAY,
          detail="Chess.com returned an unexpected response",
      ) from exc

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not connect to Chess.com",
        ) from exc

    if not games:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No games were found for {username}")

    game_responses = [transform_chess_com_game(game) for game in games]
    return ImportedGamesResponse(username=username, source="chess_com", games=game_responses)