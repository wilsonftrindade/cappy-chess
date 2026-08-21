import { useState } from "react";
import type { GameSource } from "../../types/analysis"
import type { ImportedGame } from "../../types/imports";
import PgnInput from "./PgnInput";
import AccountImport from "./AccountImport";

import "./GameImport.css"


type GameImportProps = {
  onSelectImportedGame: (game: ImportedGame) => void;
  onPgnChange: (value: string) => void;
  onReviewPgn: () => void;
  isReviewLoading: boolean;
  pgn: string;
}

const GameImport = ( { onSelectImportedGame, onPgnChange, onReviewPgn, isReviewLoading, pgn }: GameImportProps) => {
  const [mode, setMode] = useState<GameSource>("chess_com")

  return (
    <div className="game-import">
      <header className="game-import__header">
        <h2>Review your game</h2>
        <p>Choose a source and find the moments that shaped the result.</p>
      </header>

      <div className="game-import__sources">
        <button
          onClick={() => setMode("chess_com")}
          aria-pressed={mode === "chess_com"}
          className={
            mode === "chess_com"
              ? "source-card source-card--active"
              : "source-card"
          }
        >
          <span className="source-card__icon" aria-hidden="true">♟</span>
          <span>Chess.com</span>
        </button>

        <button
          onClick={() => setMode("lichess")}
          aria-pressed={mode === "lichess"}
          className={
            mode === "lichess"
              ? "source-card source-card--active"
              : "source-card"
          }
        >
          <span className="source-card__icon" aria-hidden="true">♞</span>
          <span>Lichess</span>
        </button>

        <button
          onClick={() => setMode("manual")}
          aria-pressed={mode === "manual"}
          className={
            mode === "manual"
              ? "source-card source-card--active"
              : "source-card"
          }
        >
          <span className="source-card__icon" aria-hidden="true">▤</span>
          <span>PGN</span>
        </button>
      </div>

      {mode === "manual" ? (
        <PgnInput
          isLoading={isReviewLoading}
          onPgnChange={onPgnChange}
          onReviewGame={onReviewPgn}
          pgn={pgn}
        />
        ) : (
        <AccountImport
          key={mode}
          source={mode}
          onSelectGame={onSelectImportedGame}
        />)
      }
      
    </div>
  );
}

export default GameImport;
