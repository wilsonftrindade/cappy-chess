const MoveList = ({ moves, onSelectMove }) => {
    return (
        <>
            <h3>Moves</h3>
            <ol>
            {moves.map((move) => (
              <li key={move.move_number}>
                <span> {move.move_number}. </span>

                <button onClick={() => onSelectMove(move.whiteIndex)}>
                  {move.white}
                </button>

                {move.black && move.blackIndex !== null ? (
                  <button onClick={() => onSelectMove(move.blackIndex)}>
                    {move.black}
                  </button>
                ) : null}
              </li>
            ))}
          </ol>
        </>
    );
};

export default MoveList;