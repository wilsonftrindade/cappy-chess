import { useState, useEffect } from 'react'
import { parseGame } from './api/games'
import { analyzeFen, reviewMove } from './api/analysis'
import { groupMoves } from './utils/moves'
import type { ParsedGameResponse } from './types/game'
import type { AnalysisResponse, MoveReviewResponse } from './types/analysis'
import MoveList from './components/MoveList'
import ReviewBoard from './components/ReviewBoard'
import SelectedMovePanel from './components/SelectedMovePanel'
import PgnInput from './components/PgnInput'
import AnalysisPanel from './components/AnalysisPanel'
import MoveReviewPanel from './components/MoveReviewPanel'
import './App.css'


const STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

function App() {
  const [backendStatus, setBackendStatus] = useState("checking...")
  const [pgn, setPgn] = useState("")
  const [parsedGame, setParsedGame] = useState<ParsedGameResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [selectedMoveIndex, setSelectedMoveIndex] = useState<number | null>(null);
  const [analysisResult, setAnalysisResult] = useState<null | AnalysisResponse>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [moveReviewResult, setMoveReviewResult] = useState<MoveReviewResponse | null>(null);
  const [isReviewingMove, setIsReviewingMove] = useState(false);
  const [moveReviewError, setMoveReviewError] = useState<string | null>(null)


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

  const handleParseGame = async () => {
    setIsLoading(true);
    setError(null);
    setParsedGame(null);
    setSelectedMoveIndex(null);
    
    try {
      const result = await parseGame(pgn);
      setParsedGame(result);
    }
    catch (error) {
      setError("Failed to parse game");
    }
    finally {
      setIsLoading(false);
    }
  };

  const handleAnalyzeMove = async () => {
    setIsAnalyzing(true);
    setAnalysisResult(null);
    setAnalysisError(null);

    if (!parsedGame || selectedMoveIndex === null) {
      setAnalysisError("No move selected for analysis");
      setIsAnalyzing(false);
      return;
    }

    try {
      const selectedMove = parsedGame.moves[selectedMoveIndex];
      const result = await analyzeFen(selectedMove.fen_before, 17);
      setAnalysisResult(result);
    } 
    catch (error) {
      setAnalysisError("Failed to analyze move");
    }
    finally {
      setIsAnalyzing(false);
    }
  }

  const handleReviewMove = async () => {
    setIsReviewingMove(true);
    setMoveReviewResult(null);
    setMoveReviewError(null);

    if (!parsedGame || selectedMoveIndex === null) {
      setAnalysisError("No move selected for analysis");
      setIsAnalyzing(false);
      return;
    }

    try {
      const selectedMove = parsedGame.moves[selectedMoveIndex]
      const moveUci = selectedMove.uci
      const result = await reviewMove(selectedMove.fen_before, moveUci, 17)
      setMoveReviewResult(result)
    }
    catch (error) {
      setMoveReviewError("Failed to review move")
    }
    finally {
      setIsReviewingMove(false) 
    }
  }

  const displayMoves = parsedGame ? groupMoves(parsedGame.moves) : [];
  const selectedMove = parsedGame && selectedMoveIndex !== null ? parsedGame.moves[selectedMoveIndex] : null;
  const boardPosition = selectedMove ? selectedMove.fen_after : STARTING_FEN;
  const chessboardOptions = {
    position: boardPosition,
    allowDragging: false
  }

  const handleNextMove = () => {
    setAnalysisResult(null);
    setAnalysisError(null);
    setMoveReviewResult(null);
    setMoveReviewError(null);


    if (!parsedGame) return;

    if (selectedMoveIndex === null) {
      setSelectedMoveIndex(0);
      return;
    } 
    
    if (selectedMoveIndex < parsedGame.moves.length - 1) {
      setSelectedMoveIndex(selectedMoveIndex + 1);
    }
  };

  const handlePreviousMove = () => {
    setAnalysisResult(null);
    setAnalysisError(null);
    setMoveReviewResult(null);
    setMoveReviewError(null);


    if (!parsedGame || selectedMoveIndex === null) return;

    if (selectedMoveIndex === 0) {
      setSelectedMoveIndex(null);
      return;
    }

    if (selectedMoveIndex > 0) {
      setSelectedMoveIndex(selectedMoveIndex - 1);
    }
  };

  const handleSelectMove = (index: number) => {
    setSelectedMoveIndex(index);
    setAnalysisResult(null);
    setAnalysisError(null);
    setMoveReviewResult(null);
    setMoveReviewError(null);
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
          onParseGame={handleParseGame} 
          isLoading={isLoading} />
      </div>

      {error && <p className="error-message">{error}</p>}

      {parsedGame ? (
        <section className="review-page">
          <section className="review-main">
            <div className="game-summary">
              <h2>Parsed Game</h2>
              <p>
                  {parsedGame.white ?? "Unknown"} vs{" "}
                  {parsedGame.black ?? "Unknown"} — {parsedGame.result ?? "*"}
              </p>
            </div>
          
            <ReviewBoard
              boardOptions={chessboardOptions}
              onPreviousMove={handlePreviousMove}
              onNextMove={handleNextMove}
              selectedMoveIndex={selectedMoveIndex}
              totalMoves={parsedGame.moves.length}
            />
            </section>

            <aside className="review-sidebar">
              <MoveList
                moves={displayMoves} 
                onSelectMove={handleSelectMove} 
              />

            {selectedMove ? (
              <div className="selected-move-panel-container">
                <SelectedMovePanel move={selectedMove} />
                
                <AnalysisPanel 
                  analysis={analysisResult} 
                  isAnalyzing={isAnalyzing} 
                  analysisError={analysisError} 
                  onAnalyzeMove={handleAnalyzeMove}
                />

                <MoveReviewPanel
                  review={moveReviewResult}
                  isReviewing={isReviewingMove}
                  reviewError={moveReviewError}
                  onReviewMove={handleReviewMove}
                />

              </div>
            ) : null}

            </aside>
        </section>
      ) : null}
    </main>
  );
}

export default App;
