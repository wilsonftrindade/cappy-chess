import { useState, useEffect } from 'react'
import { parseGame } from './api/games'
import { groupMoves } from './utils/moves'
import type { ParsedGameResponse } from './types/game'
import MoveList from './components/MoveList'
import ReviewBoard from './components/ReviewBoard'
import SelectedMovePanel from './components/SelectedMovePanel'
import PgnInput from './components/PgnInput'
import './App.css'


const STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

function App() {
  const [backendStatus, setBackendStatus] = useState("checking...")
  const [pgn, setPgn] = useState("")
  const [parsedGame, setParsedGame] = useState<ParsedGameResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [selectedMoveIndex, setSelectedMoveIndex] = useState<number | null>(null);

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
    
    try{
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

  const displayMoves = parsedGame ? groupMoves(parsedGame.moves) : [];

  const selectedMove = parsedGame && selectedMoveIndex !== null ? parsedGame.moves[selectedMoveIndex] : null;
  
  const boardPosition = selectedMove ? selectedMove.fen_after : STARTING_FEN;

  const chessboardOptions = {
    position: boardPosition,
    allowDragging: false
  }

  const handleNextMove = () => {
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
    if (!parsedGame || selectedMoveIndex === null) return;

    if (selectedMoveIndex === 0) {
      setSelectedMoveIndex(null);
      return;
    }

    if (selectedMoveIndex > 0) {
      setSelectedMoveIndex(selectedMoveIndex - 1);
    }
  };

  return (
    <main>
       <h1>AI Chess Coach</h1>
      <p>Backend status: {backendStatus}</p>

      <PgnInput pgn={pgn} onPgnChange={setPgn} onParseGame={handleParseGame} isLoading={isLoading} />

      {error && <p>{error}</p>}

      {parsedGame ? (
        <>
            <ReviewBoard
              boardOptions={chessboardOptions}
              onPreviousMove={handlePreviousMove}
              onNextMove={handleNextMove}
              selectedMoveIndex={selectedMoveIndex}
              parsedGame={parsedGame}
            />

            <MoveList moves={displayMoves} onSelectMove={setSelectedMoveIndex} />

            {selectedMove ? (
              <SelectedMovePanel move={selectedMove} />
            ) : null}

        </>

      ) : null}

    </main>
  );
}

export default App;
