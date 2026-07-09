import type { MoveReviewResponse } from "../types/analysis";

type MoveReviewPanelProps = {
  review: MoveReviewResponse | null;
  isReviewing: boolean;
  reviewError: string | null;
  onReviewMove: () => void;
};

function formatCp(cp: number | null, mate_in: number | null) {
  if(mate_in !== null) {
    return `Mate in ${mate_in}`;
  }
  
  if (cp === null){
    return `N/A`
  }

  const pawns = cp / 100;

  if (pawns > 0) {
    return `+${pawns.toFixed(2)}`;
  }

  return pawns.toFixed(2);
}

const MoveReviewPanel = ( { review, isReviewing, reviewError, onReviewMove }: MoveReviewPanelProps ) => {
  return (
    <section className="move-review-panel">
      <h3>Move Review</h3>

      <button
        className="review-move-button"
        onClick={onReviewMove}
        disabled={isReviewing}
      >
        {isReviewing ? "Reviewing..." : "Review Move"}
      </button>

      {reviewError ? (
        <p className="move-review-error">{reviewError}</p>
      ) : null}

      {review ? (
        <div className="move-review-result">
          <p>
            <strong>Played move:</strong> {review.move_san ?? review.move_uci}
          </p>

          <p>
            <strong>Best move:</strong>{" "}
            {review.best_move_san ?? review.best_move_uci ?? "Unknown"}
          </p>

          <p>
            <strong>Eval before:</strong> {formatCp(review.eval_cp_before, review.mate_in_before)}
          </p>

          <p>
            <strong>Eval after:</strong> {formatCp(review.eval_cp_after, review.mate_in_after)}
          </p>

          <p>
            <strong>Eval loss:</strong>{" "} {formatCp(review.eval_cp_loss, null)}
          </p>

          <p>
            <strong>Win probability before: </strong> 
            {review.win_probability_before !== null ? `${(review.win_probability_before * 100).toFixed(2)}%`: "N/A"}
          </p>

          <p>
            <strong>Win probability after: </strong> 
            {review.win_probability_after !== null ? `${(review.win_probability_after * 100).toFixed(2)}%`: "N/A"}
          </p>

          <p>
            <strong>Win probability loss: </strong>{" "}
            {review.win_probability_loss !== null ? `${(review.win_probability_loss * 100).toFixed(2)}%` : "N/A"}
          </p>


          <p>
            <strong>Classification:</strong>{" "}
            <span className="move-review-classification">
              {review.classification ?? "Unknown"}
            </span>
          </p>
        </div>
      ) : null}
    </section>
  );
}

export default MoveReviewPanel;