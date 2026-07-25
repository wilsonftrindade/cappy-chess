import { Chessboard } from 'react-chessboard';

type ReviewBoardProps = {
   boardOptions: any;
   onPreviousMove: () => void;
   onNextMove: () => void;
   selectedMoveIndex: number | null;
   totalMoves: number;
};

const ReviewBoard = ( { boardOptions, onPreviousMove, onNextMove, selectedMoveIndex, totalMoves }: ReviewBoardProps ) => {
  return (
    <section className="review-board">
      <h3>Chessboard</h3>

      <div className="board-container">
        <Chessboard options={boardOptions} />
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