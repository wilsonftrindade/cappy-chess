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

  const importControllerRef = useRef<AbortController | null>(null);

  const handleFetchGames = async () => {
    const trimmedUsername = username.trim();
    
    if (!trimmedUsername) {
      return;
    }

    importControllerRef.current?.abort();
    const controller = new AbortController();
    importControllerRef.current = controller;
    setGames([])
    setError(null)
    setLoading(true)

    try {
      const importedGames = await getImportedGames(source, trimmedUsername, 20, controller.signal)
      setGames(importedGames.games)
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

  return (
    <div className="account-import">
      <label>
        {source === "chess_com"
          ? "Chess.com username"
          : "Lichess username"}
      </label>

      <input
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
          ? "Fetching Games..."
          : "Fetch Recent Games"}
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
    </div>
  );
};

export default AccountImport;