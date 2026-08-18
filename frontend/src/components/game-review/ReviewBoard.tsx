import { Chessboard } from 'react-chessboard';
import EvalBar from "./EvalBar";

type ReviewBoardProps = {
  boardOptions: any;
  onPreviousMove: () => void;
  onNextMove: () => void;
  selectedMoveIndex: number | null;
  totalMoves: number;
  whiteWinProbability: number;
  evaluationCp: number;
  mateIn: number | null;
};

const ReviewBoard = ( { boardOptions, onPreviousMove, onNextMove, selectedMoveIndex, totalMoves, whiteWinProbability, evaluationCp, mateIn }: ReviewBoardProps ) => {
  return (
    <section className="review-board">
      <h3>Chessboard</h3>

      <div className="board-with-eval">
        <EvalBar
          whiteWinProbability={whiteWinProbability}
          evaluationCp={evaluationCp}
          mateIn={mateIn}
        />

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