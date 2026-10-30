import { useState, useRef } from "react";
import type { ImportedGame } from "../../types/imports";
import { getImportedGames } from "../../api/imports";

import "./AccountImport.css"

type AccountImportProps = {
  source: "chess_com" | "lichess";
  onSelectGame: (game: ImportedGame) => void;
}

const AccountImport = ({ source, onSelectGame }: AccountImportProps) => {
  const [username, setUsername] = useState("")
  const [games, setGames] = useState<ImportedGame[]>([])
  const [isLoading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [nextCursor, setNextCursor] = useState<string | null>(null)

  const importControllerRef = useRef<AbortController | null>(null);

  const handleFetchGames = async () => {
    const trimmedUsername = username.trim();
    
    if (!trimmedUsername) {
      return;
    }

    importControllerRef.current?.abort();
    const controller = new AbortController();
    importControllerRef.current = controller;
    setGames([]);
    setError(null);
    setLoading(true);

    try {
      const importedGames = await getImportedGames(source, trimmedUsername, 20, null, controller.signal)
      setGames(importedGames.games)
      setNextCursor(importedGames.next_cursor)
    }
    catch (error) {
      if (error instanceof DOMException && error.name === "AbortError") {
        return;
      }

      if (error instanceof Error) {
        setError(error.message)
      }

      else {
        setError("An unknown error occurred while fetching games")
      }
    }
    finally {
      setLoading(false)
      if (importControllerRef.current === controller) {
        importControllerRef.current = null;
      }
    }
  };

  const handleLoadMore = async () => {
    if (!nextCursor) {
      return;
    }

    importControllerRef.current?.abort();
    const controller = new AbortController();
    importControllerRef.current = controller;

    const trimmedUsername = username.trim();

    setError(null);
    setLoading(true);

    try {
      const newImportedGames = await getImportedGames(source, trimmedUsername, 20, nextCursor, controller.signal)
      setGames(games.concat(newImportedGames.games));
      setNextCursor(newImportedGames.next_cursor);
    }

    catch (error) {
      if (error instanceof DOMException && error.name === "AbortError") {
        return;
      }

      if (error instanceof Error) {
        setError(error.message);
      }

      else {
        setError("Failed to fetch more games");
      }
    }
    finally {
      setLoading(false)
      if (importControllerRef.current === controller) {
        importControllerRef.current = null;
      }
    }
  };
  
  return (
    <div className="account-import">
      <label htmlFor="account-username">
        {source === "chess_com"
          ? "Chess.com username"
          : "Lichess username"}
      </label>

      <input
        id="account-username"
        value={username}
        onChange={(event) =>
          setUsername(event.target.value)
        }
        placeholder="Enter username"
      />

      <button
        onClick={handleFetchGames}
        disabled={isLoading || !username.trim()}
      >
        {isLoading
          ? "Importing Games..."
          : "Import Recent Games"}
      </button>

      {error && (
        <p className="import-error">
          {error}
        </p>
      )}

      <div className="imported-games">
        {games.map((game) => (
          <button
            key={game.external_id}
            className="imported-game"
            onClick={() => onSelectGame(game)}
          >
            <div className="imported-game__player">
              <span>{game.white}</span>

              {game.white_elo !== null && (
                <span className="imported-game__rating">
                  {game.white_elo}
                </span>
              )}
            </div>

            <div className="imported-game__player">
              <span>{game.black}</span>

              {game.black_elo !== null && (
                <span className="imported-game__rating">
                  {game.black_elo}
                </span>
              )}
            </div>

            <div className="imported-game__footer">
              <span className="imported-game__result">
                {game.result}
              </span>

              <span className="imported-game__time-class">
                {game.time_class}
              </span>
            </div>
          </button>
        ))}
      </div>

      {nextCursor && (
        <button
          type="button"
          onClick={handleLoadMore}
          disabled={isLoading}
        >
          {isLoading
            ? "Loading..."
            : "Load More"}
        </button>
      )}

    </div>
  );
};

export default AccountImport;
