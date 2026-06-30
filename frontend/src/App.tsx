import { useState, useEffect } from 'react'
import { parseGame } from './api/games'
import type { ParsedGameResponse } from './types/game'
import './App.css'

function App() {
  const [backendStatus, setBackendStatus] = useState("checking...")
  const [pgn, setPgn] = useState("")
  const [parsedGame, setParsedGame] = useState<ParsedGameResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

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

          <h3>Moves</h3>
          <ol>
            {parsedGame.moves.map((move, index) => (
              <li key={index}>
                {move.move_number}. {move.color} {move.san} ({move.uci})
              </li>
            ))}
          </ol>
        </section>
      )}
    </main>
  );
}

export default App;
