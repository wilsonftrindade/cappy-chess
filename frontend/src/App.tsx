import { useState, useEffect } from 'react'
import { parseGame } from './api/games'
import type { ParsedGameResponse, ParsedMove, DisplayMove } from './types/game'
import './App.css'
import { Chessboard } from 'react-chessboard'

const STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

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

  function groupMoves(moves: ParsedMove[]): DisplayMove[] {
    const displayMoves: DisplayMove[] = [];

    for (let i = 0; i < moves.length; i += 2) {
      const moveNumber = moves[i].move_number;
      const whiteMove = moves[i].san;
      const blackMove = (i + 1 < moves.length) ? moves[i + 1].san : null;

      const displayMove = {
        move_number: moveNumber,
        white: whiteMove,
        black: blackMove,
        whiteIndex: i,
        blackIndex: (i + 1 < moves.length) ? i + 1 : null
      };

      displayMoves.push(displayMove);
    }

    return displayMoves;
  }

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

      <section>
        <h2>Paste PGN</h2>

        <textarea
          value={pgn}
          onChange={(event) => setPgn(event.target.value)}
          rows={10}
          cols={80}
          placeholder="Paste a PGN here..."
        />

        <br />

        <button onClick={handleParseGame} disabled={isLoading || !pgn.trim()}>
          {isLoading ? "Parsing..." : "Parse Game"}
        </button>
      </section>

      {error && <p>{error}</p>}

      {parsedGame && (
        <section>
          <h2>Parsed Game</h2>
          <p>
            {parsedGame.white ?? "Unknown"} vs{" "}
            {parsedGame.black ?? "Unknown"} — {parsedGame.result ?? "*"}
          </p>

          <section>
            <h3>Chessboard</h3>
            <div style={{ width: "600px", height: "600px"}}>
              <Chessboard options={chessboardOptions} />
            </div>

            <button onClick={handlePreviousMove} disabled={selectedMoveIndex == null}>
              Previous
            </button>

            <button onClick={handleNextMove} disabled={selectedMoveIndex === parsedGame.moves.length - 1}>
              Next
            </button>
          </section>

          <h3>Moves</h3>
          <ol>
            {displayMoves.map((move) => (
              <li key={move.move_number}>
                <span> {move.move_number}. </span>

                <button onClick={() => setSelectedMoveIndex(move.whiteIndex)}>
                  {move.white}
                </button>

                {move.black && move.blackIndex !== null ? (
                  <button onClick={() => setSelectedMoveIndex(move.blackIndex)}>
                    {move.black}
                  </button>
                ) : null}
              </li>
            ))}
          </ol>

          <ul>
            {parsedGame.moves.map((move, index) => (
              <li key={index} onClick={() => setSelectedMoveIndex(index)}>
                {move.move_number}. {move.color} {move.san}
              </li>
            ))}
          </ul>

            {selectedMove && (
              <section>
                <h3>Selected Move</h3>
                <p>
                  {selectedMove.move_number}. {selectedMove.color} {selectedMove.san}
                </p>
                <p> UCI: {selectedMove.uci}</p>
                <p>FEN before: {selectedMove.fen_before}</p>
                <p>FEN after: {selectedMove.fen_after}</p>
              </section>
            )}

        </section>
      )}
    </main>
  );
}

export default App;
