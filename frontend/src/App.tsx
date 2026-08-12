import { useState, useEffect, useRef } from 'react'
import type { ParsedGameResponse } from './types/game'
import { createReviewJob, getReviewJob, getPersistedReview } from './api/analysis'
import type { GameReviewResponse } from './types/analysis'
import type { ReviewJob } from './types/reviewJob'
import GameReviewPage from './components/game-review/GameReviewPage'
import PgnInput from './components/pgn/PgnInput'
import AnalysisOverlay from './components/common/AnalysisOverlay'
import { parseGame } from './api/games'

import './App.css'
import AnalysisPreviewPage from './components/game-review/AnalysisPreviewPage'

const STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function App() {
  const [backendStatus, setBackendStatus] = useState("checking...")

  const [pgn, setPgn] = useState("")
  const [parsedGame, setParsedGame] = useState<ParsedGameResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [gameReview, setGameReview] = useState<GameReviewResponse | null>(null)

  const[reviewJob, setReviewJob] = useState<null | ReviewJob>(null)
  const pollingControllerRef = useRef<AbortController | null>(null);

  // Health check for the backend server
  useEffect(() => {
    const fetchBackendData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/health')

        if (!response.ok) {
          throw new Error('Network response was not ok')
        }

        const result = await response.json()
        setBackendStatus(result.status)

      } catch (error) {
        console.error('Error fetching backend data:', error)
        setBackendStatus("error")
      }
    };

    fetchBackendData();
  }, []);

  useEffect(() => {
    return () => {
      if (pollingControllerRef.current) {
        pollingControllerRef.current.abort();
      }
    };
  }, []);

  const handleReviewGame = async () => {

    pollingControllerRef.current?.abort();
    const controller = new AbortController();
    pollingControllerRef.current = controller;
    setParsedGame(null);
    setReviewJob(null);
    setGameReview(null);
    setError (null);
    setIsLoading(true);

    try {
      const parsedGameResult = await parseGame(pgn, controller.signal);
      setParsedGame(parsedGameResult);
    }
    catch (error) {
      if (error instanceof DOMException && error.name === "AbortError") {
        return;
      }
      setError("Failed to parse game");
    }

    try {
      const createdJob = await createReviewJob(pgn, 17, controller.signal);
      if (createdJob.status === "completed") {
        const persistedReview =  await getPersistedReview(createdJob.job_id, controller.signal);
         if (persistedReview.result === null) {
          setError("Review completed but no persisted result was found");
        }

        setGameReview(persistedReview.result);
        return;
      }

      if (createdJob.status === "failed") {
        const persistedReview =  await getPersistedReview(createdJob.job_id, controller.signal);
        setError(persistedReview.error || "Review job failed");
        return;
      }
      
      while (!controller.signal.aborted) {
        const currentJob = await getReviewJob(createdJob.job_id, controller.signal);
        setReviewJob(currentJob);
        
        if (currentJob.status === "completed") {
          const currentReview = await getPersistedReview(
            createdJob.job_id,
            controller.signal
          );

          if (currentReview.result === null) {
            setError("Review completed but no persisted result was found");
            break;
          }

          setGameReview(currentReview.result);
          break;

        } else if (currentJob.status === "failed") {
          setError(currentJob.error || "Game review job failed");
          break;
        }

        await delay(500); // Poll every half a second
     }
   }

    catch(error: unknown) {
      if (error instanceof DOMException && error.name === "AbortError") {
        return;
      } 
      
      if (error instanceof Error) {
        setError(error.message);
      }
      else {
        setError("An unknown error occurred while reviewing the game");
      }
   }

    finally {
      if (pollingControllerRef.current === controller) {
        pollingControllerRef.current = null;
      }
        setIsLoading(false);
    }
  };

  const completedPlies = reviewJob?.completed_plies ?? 0;
  const previewMoveIndex = completedPlies > 0 ? completedPlies - 1 : 0; 
  const previewBoardFEN = 
    parsedGame === null
      ? STARTING_FEN
      : previewMoveIndex === null
        ? parsedGame.moves[0]?.fen_before ??
          STARTING_FEN
        : parsedGame.moves[previewMoveIndex]
            ?.fen_after ?? STARTING_FEN;


  return (
    <main className="app">
      <header className="app-header">
        <h1>AI Chess Coach</h1>
        <p>Backend status: {backendStatus}</p>
      </header>

      <AnalysisOverlay
        isVisible={isLoading}
        reviewJob={reviewJob} />

      <div className="pgn-input-container"> 
        <PgnInput 
          pgn={pgn} 
          onPgnChange={setPgn} 
          onAnalyzeGame={handleReviewGame} 
          isLoading={isLoading} />
      </div>

      {error && <p className="error-message">{error}</p>}

      {isLoading && parsedGame ? (
        <AnalysisPreviewPage
          parsedGame={parsedGame}
          boardPosition={previewBoardFEN}
          currentMoveIndex={previewMoveIndex} />
      ) : gameReview ? (
        <GameReviewPage gameReview={gameReview} />
      ) : null}

    </main>
  );
}

export default App;
