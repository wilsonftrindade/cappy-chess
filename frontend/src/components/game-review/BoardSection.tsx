import ReviewBoard from "./ReviewBoard"
import PlayerInfo from "./PlayerInfo"
import type { GameReviewResponse } from "../../types/analysis"

type BoardSectionProps = {
  gameReview: GameReviewResponse;
  boardPosition: string;
  onPreviousMove: () => void;
  onNextMove: () => void;
  selectedMoveIndex: number | null;
}

const BoardSection = ( { gameReview, boardPosition, onPreviousMove, onNextMove, selectedMoveIndex } : BoardSectionProps)  => {

  const boardOptions = {
    position: boardPosition,
    allowDragging: false
  }

  return (
    <section className="board-section">
      <PlayerInfo
        name={gameReview.black}
        elo={gameReview.black_elo}
        color="black"
      />

      <ReviewBoard
        boardOptions = {boardOptions}
        onPreviousMove={onPreviousMove}
        onNextMove={onNextMove}
        selectedMoveIndex={selectedMoveIndex}
        totalMoves={gameReview.reviewed_moves.length}
      />

      <PlayerInfo
        name={gameReview.white}
        elo={gameReview.white_elo}
        color="white"
      />
    </section>
  )

};

export default BoardSection;