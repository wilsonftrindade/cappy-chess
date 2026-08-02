import { useState, useEffect, useRef } from 'react'
import { createReviewJob, getReviewJob } from './api/analysis'
import type { GameReviewResponse } from './types/analysis'
import type { ReviewJob } from './types/reviewJob'
import GameReviewPage from './components/game-review/GameReviewPage'
import PgnInput from './components/pgn/PgnInput'
import './App.css'

function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function App() {
  const [backendStatus, setBackendStatus] = useState("checking...")

  const [pgn, setPgn] = useState("")
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

    setReviewJob(null);
    setGameReview(null);
    setError (null);
    setIsLoading(true);

    try {
      const createdJob = await createReviewJob(pgn, 17, controller.signal);
      
      while (!controller.signal.aborted) {
        const currentJob = await getReviewJob(createdJob.job_id, controller.signal);
        setReviewJob(currentJob);
        
        if (currentJob.status === "completed") {
          if (currentJob.result === null) {
            setError("Job completed but no result was returned");
            break;
          }
          setGameReview(currentJob.result);
          break;

        } else if (currentJob.status === "failed") {
          setError(currentJob.error || "Game review job failed");
          break;
        }

        await delay(1000); // Poll every second
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

  return (
    <main className="app">
      <header className="app-header">
        <h1>AI Chess Coach</h1>
        <p>Backend status: {backendStatus}</p>
      </header>

      <div className="pgn-input-container"> 
        <PgnInput 
          pgn={pgn} 
          onPgnChange={setPgn} 
          onAnalyzeGame={handleReviewGame} 
          isLoading={isLoading} />
      </div>

      {reviewJob && isLoading && (
        <div>
          <p>Status: {reviewJob.status}</p>

          <p>
            Progress: {reviewJob.completed_plies}
            {" / "}
            {reviewJob.total_plies ?? "unknown"}
          </p>
        </div>
      )}

      {error && <p className="error-message">{error}</p>}

      {gameReview ? (
        <GameReviewPage gameReview={gameReview} />
      ) : null}
    </main>
  );
}

export default App;
