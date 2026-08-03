import type { ParsedGameResponse } from "../../types/game";
import { groupMoves } from "../../utils/moves";
import PlayerInfo from "./PlayerInfo";
import ReviewBoard from "./ReviewBoard";
import MoveList from "./MoveList";

type AnalysisPreviewPageProps = {
  parsedGame: ParsedGameResponse;
  boardPosition: string;
  currentMoveIndex: number | null;
};

function AnalysisPreviewPage({
  parsedGame,
  boardPosition,
  currentMoveIndex,
}: AnalysisPreviewPageProps) {
  const displayMoves = groupMoves(parsedGame.moves);

  const boardOptions = {
    position: boardPosition,
    allowDragging: false,
  };

  return (
    <div className="game-review-page">
      <div className="board-container">
        <section className="board-section">
          <PlayerInfo
            name={parsedGame.black}
            elo={parsedGame.black_elo}
            color="black"
          />

          <ReviewBoard
            boardOptions={boardOptions}
            onPreviousMove={() => {}}
            onNextMove={() => {}}
            selectedMoveIndex={currentMoveIndex}
            totalMoves={parsedGame.moves.length}
          />

          <PlayerInfo
            name={parsedGame.white}
            elo={parsedGame.white_elo}
            color="white"
          />
        </section>
      </div>

      <aside className="review-sidebar">
        <header className="review-sidebar-header">
          <h2>Game Review</h2>
        </header>

        <MoveList
          moves={displayMoves}
          selectedMoveIndex={currentMoveIndex}
          onSelectMove={() => {}}
        />
      </aside>
    </div>
  );
}

export default AnalysisPreviewPage;