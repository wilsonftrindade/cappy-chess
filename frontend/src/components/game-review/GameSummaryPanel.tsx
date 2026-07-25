import type { GameReviewResponse } from "../../types/analysis";

const CLASSIFICATIONS = [
  "Best",
  "Excellent",
  "Good",
  "Inaccuracy",
  "Mistake",
  "Blunder",
] as const;

type GameSummaryPanelProps = {
  gameReview: GameReviewResponse;
  onStartReview: () => void;
}

function formatAccuracy(accuracy: number | null) {
  if (accuracy === null) {
      return "N/A"
  }

  return `${(accuracy.toFixed(1))}%`
}

const GameSummaryPanel = ( { gameReview, onStartReview }: GameSummaryPanelProps ) => {
  const whiteSummary = gameReview.white_summary;
  const blackSummary = gameReview.black_summary;

  return (
    <section className="game-summary-panel">
      <header className="game-summary-header">
        <h2>Game Summary</h2>

        <p> {gameReview.white} vs {gameReview.black}</p>

        <p>Result: {gameReview.result}</p>
      </header>

      <div className="accuracy-summary">
        <span>Accuracy</span>

        <div className="player-accuracy">
          <span>{gameReview.white}</span>
          <strong>
              {formatAccuracy(whiteSummary.accuracy)}
          </strong>
        </div>

        <div className="player-accuracy">
          <span>{gameReview.black}</span>
          <strong>
              {formatAccuracy(blackSummary.accuracy)}
          </strong>
        </div>
      </div>

      <div className="classification-summary">
          {CLASSIFICATIONS.map((classification) => (
          <div className="classification-row" key={classification}>
            <span>
              {gameReview.white_summary
                .classification_counts[classification] ?? 0}
            </span>

            <strong>{classification}</strong>

            <span>
              {gameReview.black_summary
                .classification_counts[classification] ?? 0}
            </span>
          </div>
        ))}
      </div>

      <button className="start-review-button" onClick={onStartReview} disabled={gameReview.reviewed_moves.length === 0}>
        Start Review
      </button>
    </section>
  )
};

export default GameSummaryPanel;