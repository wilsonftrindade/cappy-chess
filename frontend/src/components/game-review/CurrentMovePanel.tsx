import type { ReviewedMove } from "../../types/analysis";

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
  return (
    <section className="current-move-panel">
      <div className="played-move-review">
        <div>
          <strong> {move.move_san ?? move.move_uci} </strong> {" "} 
          is {move.classification?.toLowerCase() ?? "unclassified"}
        </div>

        <span className="evaluation-badge">
          {formatEvaluation(move.eval_cp_after, move.mate_in_after)}
        </span>
      </div>

      {(move.classification !== "Best") ? (
        <div className="best-move-review">
        <div>
          <strong>{move.best_move_san ?? "No best move"}</strong>{" "}
          was best
        </div>

        <span className="evaluation-badge">
          {formatEvaluation(
            move.eval_cp_before,
            move.mate_in_before
          )}
        </span>
      </div>
      ) : null}

      <div className="move-review-details">
        <p>
          <strong>Move accuracy:</strong>{" "}
          {move.move_accuracy !== null
            ? `${move.move_accuracy.toFixed(1)}%`
            : "N/A"}
        </p>

        <p>
          <strong>Win probability loss:</strong>{" "}
          {move.win_probability_loss !== null
            ? `${(
                move.win_probability_loss * 100
              ).toFixed(2)}%`
            : "N/A"}
        </p>
      </div>
  </section>
  );
};

export default CurrentMovePanel;