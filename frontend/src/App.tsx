import { useState, useEffect } from 'react'
import { reviewGame } from './api/analysis'
import type { GameReviewResponse } from './types/analysis'
import GameReviewPage from './components/game-review/GameReviewPage'
import PgnInput from './components/pgn/PgnInput'
import './App.css'

function App() {
  const [backendStatus, setBackendStatus] = useState("checking...")

  const [pgn, setPgn] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [gameReview, setGameReview] = useState<GameReviewResponse | null>(null)

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


  const handleReviewGame = async () => {
    setGameReview(null);
    setError (null);
    setIsLoading(true);

    try {
      const result = await reviewGame(pgn, 17)
      setGameReview(result)
    }
    catch (error) {
      setError("Failed to review game")
    }
    finally {
      setIsLoading(false) 
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

      {error && <p className="error-message">{error}</p>}

      {gameReview ? (
        <GameReviewPage gameReview={gameReview} />
      ) : null}
    </main>
  );
}

export default App;
