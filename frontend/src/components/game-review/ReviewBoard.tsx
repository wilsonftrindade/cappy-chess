import { Chessboard } from 'react-chessboard';
import EvalBar from "./EvalBar";


type EvalDisplay = {
  whiteWinProbability: number;
  evaluationCp: number;
  mateIn: number | null;
}

type ReviewBoardProps = {
  boardOptions: any;
  onPreviousMove: () => void;
  onNextMove: () => void;
  selectedMoveIndex: number | null;
  totalMoves: number;
  evaluation?: EvalDisplay
};

const ReviewBoard = ( { boardOptions, onPreviousMove, onNextMove, selectedMoveIndex, totalMoves, evaluation}: ReviewBoardProps ) => {
  return (
    <section className="review-board">
      <h3>Chessboard</h3>

      <div className="board-with-eval">
        {evaluation ? (
          <EvalBar
            whiteWinProbability={evaluation.whiteWinProbability}
            evaluationCp={evaluation.evaluationCp}
            mateIn={evaluation.mateIn}
          />
        ) : null}
        
        <div className="board-container">
          <Chessboard options={boardOptions} />
        </div>
      </div>

      <div className="board-controls">
        <button onClick={onPreviousMove} disabled={selectedMoveIndex == null}>
        Previous
        </button>

        <button onClick={onNextMove} disabled={selectedMoveIndex === totalMoves - 1}>
        Next
        </button>
      </div>
    </section>
  );
};

export default ReviewBoard;