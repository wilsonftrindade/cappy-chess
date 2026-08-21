import type { ReviewedMove } from "../../types/analysis";
import { getClassificationDetails } from "../../utils/moveClassifications";

type CurrentMovePanelProps = {
    move: ReviewedMove;
}

function formatEvaluation(evaluation: number | null, mate_in: number | null): string {

  if (mate_in !== null) {
    return `Mate in ${mate_in}`;
  }

  if (evaluation === null) {
    return "Evaluation not available";
  }
  
  const eval_score = evaluation / 100; 

  if (eval_score > 0) {
    return `+${eval_score.toFixed(2)}`;
  }

  return `${eval_score.toFixed(2)}`;
};

const CurrentMovePanel = ( { move }: CurrentMovePanelProps ) => {
  const playedMoveDetails = getClassificationDetails(move.classification);
  const bestMoveDetails = getClassificationDetails("Best");

  return (
    <section className="current-move-panel">
      <div className="played-move-review">
        <div className={`move-review-label move-tier--${playedMoveDetails?.slug ?? "neutral"}`}>
          {playedMoveDetails ? (
            <span
              className="classification-icon"
              style={{ backgroundImage: `url(${playedMoveDetails.icon})` }}
              aria-hidden="true"
            />
          ) : null}

          <span>
            <strong>{move.move_san ?? move.move_uci}</strong>{" "}
            is{" "} 
            {move.classification?.toLowerCase() === "inaccuracy"
              ? "an "
              : ["mistake", "blunder"].includes(
                  move.classification?.toLowerCase() ?? ""
                )
                ? "a "
                : ""}
            {move.classification?.toLowerCase() ?? "unclassified"}
          </span>
          
        </div>

        <span className="evaluation-badge">
          {formatEvaluation(move.eval_cp_after, move.mate_in_after)}
        </span>
      </div>

      {(move.classification !== "Best") ? (
        <div className="best-move-review">
          <div className="move-review-label move-tier--best">
            {bestMoveDetails ? (
              <span
                className="classification-icon"
                style={{ backgroundImage: `url(${bestMoveDetails.icon})` }}
                aria-hidden="true"
              />
            ) : null}

            <span>
              <strong>{move.best_move_san ?? "No best move"}</strong>{" "}
              was best
            </span>
          </div>

          <span className="evaluation-badge">
            {formatEvaluation(
              move.eval_cp_before,
              move.mate_in_before
            )}
          </span>
        </div>
      ) : null}

  </section>
  );
};

export default CurrentMovePanel;
