import type { ReviewedMove}  from "../../types/analysis"
import { groupMoves } from "../../utils/moves"
import CurrentMovePanel from "./CurrentMovePanel"
import MoveList from "./MoveList"

type ActiveReviewPanelProps = {
  reviewedMoves: ReviewedMove[];
  selectedMove: ReviewedMove | null;
  selectedMoveIndex: number | null;
  onSelectMove: (index: number) => void;
  onSummary: () => void;
}

const ActiveReviewPanel = ( { reviewedMoves, selectedMove, selectedMoveIndex, onSelectMove, onSummary }: ActiveReviewPanelProps ) => {
  const displayMoves = groupMoves(reviewedMoves);

  return (
    <section className="active-review-panel">
      {selectedMove ? (
          <CurrentMovePanel move={selectedMove} />
        ) : (
          <p>Select a move to begin reviewing.</p>
        )
      }

      <MoveList
        moves={displayMoves}
        selectedMoveIndex={selectedMoveIndex}
        onSelectMove={onSelectMove}
      />

      <button className="go-to-summary-button" onClick={onSummary}>
        Game Summary
      </button>
    </section>
  );
};

export default ActiveReviewPanel;
      