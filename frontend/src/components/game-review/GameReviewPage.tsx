import "./GameReviewPage.css";
import "./ReviewPanels.css";
import { useState } from 'react';
import type { GameReviewResponse } from "../../types/analysis";
import BoardSection from "./BoardSection";
import GameSummaryPanel from "./GameSummaryPanel";
import ActiveReviewPanel from './ActiveReviewPanel';
import EvalGraph from './EvalGraph'

const STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

type GameReviewProps = {
    gameReview: GameReviewResponse;
}

type ReviewMode = "summary" | "reviewing"

const GameReviewPage = ({ gameReview }: GameReviewProps) => {
  const [selectedMoveIndex, setSelectedMoveIndex] = useState<number | null>(null);
  const [reviewMode, setReviewMode] = useState<ReviewMode>("summary")

  const handleStartReview = () => {
    if (gameReview.reviewed_moves.length === 0) {
      return;
    }

    setReviewMode("reviewing")
    setSelectedMoveIndex(0)
  }

  const handleNextMove = () => {
    if (selectedMoveIndex === null) {
      setSelectedMoveIndex(0);
      setReviewMode("reviewing");
      return;
    } 
    
    if (selectedMoveIndex < gameReview.reviewed_moves.length - 1) {
      setSelectedMoveIndex(selectedMoveIndex + 1);
    }

    setReviewMode("reviewing");
  };

  const handlePreviousMove = () => {
    if (selectedMoveIndex === null) return;

    if (selectedMoveIndex === 0) {
      setSelectedMoveIndex(null);
    }

    if (selectedMoveIndex > 0) {
      setSelectedMoveIndex(selectedMoveIndex - 1);
    }
  };

  const handleSelectMove = (index: number) => {
    setSelectedMoveIndex(index);
  };

  const selectedMove = selectedMoveIndex !== null ? gameReview.reviewed_moves[selectedMoveIndex] : null;
  const initialPosition = gameReview.reviewed_moves[0]?.fen_before ?? STARTING_FEN;
  const boardPosition = selectedMove ? selectedMove.fen_after : initialPosition;
  const currentWinProbability = (selectedMove ? selectedMove.win_probability_after : 0.5) ?? 0.5;
  const whiteWinProbability = (selectedMove?.color === "white" ? currentWinProbability : 1 - currentWinProbability) ?? 0.5;
  const currentEvalCp =  (selectedMove ? selectedMove.eval_cp_after : 0.0) ?? 0.0;
  const currentMateIn = selectedMove ? selectedMove.mate_in_after : null

  return (
    <div className="game-review-page">
      <div className="board-column">
        <BoardSection
          gameReview={gameReview}
          boardPosition={boardPosition}
          onPreviousMove={handlePreviousMove}
          onNextMove={handleNextMove}
          selectedMoveIndex={selectedMoveIndex}
          whiteWinProbability={whiteWinProbability}
          evaluationCp={currentEvalCp}
          mateIn={currentMateIn}
        />
      </div>

      <aside className="review-sidebar">
        <header className="review-sidebar-header">
          <img className="review-brand-mark" aria-hidden="true" src="/cappychess.png" alt="Cappy Chess Logo" />

          <div>
            <h2>Game Review</h2>
            <p>Let&apos;s find the moments that shaped this game.</p>
          </div>
        </header>

        <div className="eval-graph-container">
          <div className="eval-graph-heading">
            <strong>Game momentum</strong>
            <span>Select a point to visit that move</span>
          </div>

          <EvalGraph
            reviewedMoves={gameReview.reviewed_moves}
            onSelectMove={handleSelectMove}
          />
        </div>

        {reviewMode === "summary" ? (
          <GameSummaryPanel
            gameReview={gameReview}
            onStartReview={handleStartReview}
          />
        ) : (
          <ActiveReviewPanel
            reviewedMoves={gameReview.reviewed_moves}
            selectedMove={selectedMove}
            selectedMoveIndex={selectedMoveIndex}
            onSelectMove={handleSelectMove}
            onSummary={() => setReviewMode("summary")}
          />
        )}
      </aside>

    </div>
  )
};

export default GameReviewPage;
