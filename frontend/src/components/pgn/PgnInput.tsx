import "./PgnInput.css"

type PgnInputProps = {
    isLoading: boolean;
    onPgnChange: (value: string) => void;
    onAnalyzeGame: () => void;
    pgn: string
};

const PgnInput = ( { isLoading, onPgnChange, onAnalyzeGame, pgn }: PgnInputProps) => {
    return (
        <>
        <h2>Paste PGN</h2>

        <textarea className="pgn-textarea"
          value={pgn}
          onChange={(event) => onPgnChange(event.target.value)}
          rows={10}
          cols={80}
          placeholder="Paste a PGN here..."
        />

        <br />

        <button className="parse-button" onClick={onAnalyzeGame} disabled={isLoading || !pgn.trim()}>
          {isLoading ? "Reviewing Game..." : "Review Game"}
        </button>
        </>
    );
};

export default PgnInput;