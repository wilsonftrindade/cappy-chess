type PgnInputProps = {
    isLoading: boolean;
    onPgnChange: (value: string) => void;
    onParseGame: () => void;
    pgn: string
};

const PgnInput = ( { isLoading, onPgnChange, onParseGame, pgn }: PgnInputProps) => {
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

        <button className="parse-button" onClick={onParseGame} disabled={isLoading || !pgn.trim()}>
          {isLoading ? "Parsing..." : "Parse Game"}
        </button>
        </>
    );
};

export default PgnInput;