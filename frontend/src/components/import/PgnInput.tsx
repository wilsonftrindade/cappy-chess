import "./PgnInput.css"

type PgnInputProps = {
    isLoading: boolean;
    onPgnChange: (value: string) => void;
    onReviewGame: () => void;
    pgn: string
};

const PgnInput = ( { isLoading, onPgnChange, onReviewGame, pgn }: PgnInputProps) => {
    return (
      <section className="pgn-input">
        <h2>Paste a PGN</h2>
        <p className="pgn-input__hint">Use a complete game exported from your chess platform.</p>

        <textarea className="pgn-textarea"
          value={pgn}
          onChange={(event) => onPgnChange(event.target.value)}
          rows={10}
          cols={80}
          placeholder="Paste a PGN here..."
        />

        <button className="parse-button" onClick={onReviewGame} disabled={isLoading || !pgn.trim()}>
          {isLoading ? "Reviewing Game..." : "Review Game"}
        </button>
      </section>
    );
};

export default PgnInput;
