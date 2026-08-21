import type { GameReviewResponse } from "../../types/analysis";
import { getClassificationDetails } from "../../utils/moveClassifications";

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
        <div>
          <h2>Game summary</h2>
          <p>{gameReview.white} vs {gameReview.black}</p>
        </div>

        <span className="game-result">{gameReview.result}</span>
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
        {CLASSIFICATIONS.map((classification) => {
          const details = getClassificationDetails(classification);

          return (
            <div
              className={`classification-row move-tier--${details?.slug ?? "neutral"}`}
              key={classification}
            >
              <span>
                {gameReview.white_summary
                  .classification_counts[classification] ?? 0}
              </span>

              <strong className="classification-label">
                {details ? (
                  <span
                    className="classification-icon"
                    style={{ backgroundImage: `url(${details.icon})` }}
                    aria-hidden="true"
                  />
                ) : null}

                <span>{classification}</span>
              </strong>

              <span>
                {gameReview.black_summary
                  .classification_counts[classification] ?? 0}
              </span>
            </div>
          );
        })}
      </div>

      <button className="start-review-button" onClick={onStartReview} disabled={gameReview.reviewed_moves.length === 0}>
        Start Review
      </button>
    </section>
  )
};

export default GameSummaryPanel;
