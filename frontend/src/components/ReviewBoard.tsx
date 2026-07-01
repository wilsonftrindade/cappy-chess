import { Chessboard } from 'react-chessboard'

const ReviewBoard = ( { boardOptions, onPreviousMove, onNextMove, selectedMoveIndex, parsedGame } ) => {
    return (
        <>
            <h2>Parsed Game</h2>
            
            <p>
                {parsedGame.white ?? "Unknown"} vs{" "}
                {parsedGame.black ?? "Unknown"} — {parsedGame.result ?? "*"}
            </p>

            <h3>Chessboard</h3>
            <div style={{ width: "600px", height: "600px"}}>
                <Chessboard options={boardOptions} />
            </div>

            <button onClick={onPreviousMove} disabled={selectedMoveIndex == null}>
              Previous
            </button>

            <button onClick={onNextMove} disabled={selectedMoveIndex === parsedGame.moves.length - 1}>
              Next
            </button>
        </>
        
    );
};

export default ReviewBoard;