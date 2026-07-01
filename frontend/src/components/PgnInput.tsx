const PgnInput = ( {isLoading, onPgnChange, onParseGame, pgn} ) => {
    return (
        <>
        <h2>Paste PGN</h2>

        <textarea
          value={pgn}
          onChange={(event) => onPgnChange(event.target.value)}
          rows={10}
          cols={80}
          placeholder="Paste a PGN here..."
        />

        <br />

        <button onClick={onParseGame} disabled={isLoading || !pgn.trim()}>
          {isLoading ? "Parsing..." : "Parse Game"}
        </button>
        </>
    );
};

export default PgnInput;