import httpx
from fastapi import APIRouter, HTTPException, status, Query
from app.schemas.imports import ImportedGamesResponse, ImportedSource
from app.services.imports.chess_com import fetch_chess_com_games, transform_chess_com_game
from app.services.imports.lichess import fetch_lichess_games, transform_lichess_game


router = APIRouter()

@router.get("/{source}/{username}/games", response_model=ImportedGamesResponse)
async def get_imported_games(source: ImportedSource, username: str, limit: int = Query(default=20, ge=1, le=50)):
	try: 
		if (source == "chess-com"):
			games = await fetch_chess_com_games(username, limit)
			game_responses = [transform_chess_com_game(game) for game in games]
			game_source = "chess_com"

		elif (source == "lichess"):
			games = await fetch_lichess_games(username, limit)
			game_responses = [transform_lichess_game(game) for game in games]
			game_source = "lichess"

		return ImportedGamesResponse(username=username, source=game_source, games=game_responses)

	except httpx.HTTPStatusError as exc:
		if source == "chess-com":
			provider = "Chess.com"
		elif source == "lichess":
			provider = "Lichess"

		if exc.response.status_code == 404:
					raise HTTPException(
						status_code=status.HTTP_404_NOT_FOUND,
						detail=f"{username} not found",
					) from exc

		if exc.response.status_code == 429:
				raise HTTPException(
					status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
					detail=f"{provider} is temporarily rate limiting requests",
				) from exc

		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail=f"{provider} returned an unexpected response",
		) from exc

	except httpx.RequestError as exc:
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail=f"Could not connect to {provider}",
		) from exc