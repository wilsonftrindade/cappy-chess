import type { ParsedMove } from "../types/game";

type MoveListProps = {
    moves: ParsedMove[];
    onSelectMove: (index: number) => void;}

const MoveList = ( { moves, onSelectMove }: MoveListProps ) => {
    return (
        <section className="move-list-container">
            <h3>Moves</h3>

          <div className="move-list">
            {moves.map((move) => (
              <div className="move-row" key={move.move_number}>
                <span> {move.move_number}. </span>

                <button className="move-button" onClick={() => onSelectMove(move.whiteIndex)}>
                  {move.white}
                </button>

                {move.black && move.blackIndex !== null ? (
                  <button className="move-button" onClick={() => onSelectMove(move.blackIndex)}>
                    {move.black}
                  </button>
                ) : null}
              </div>
            ))}
          </div>
        </section>
    );
};

export default MoveList;