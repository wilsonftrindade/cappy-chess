import type { DisplayMove } from "../../types/game";

type MoveListProps = {
    moves: DisplayMove[];
    selectedMoveIndex: number | null;
    onSelectMove: (index: number) => void;
  }

const MoveList = ( { moves, selectedMoveIndex, onSelectMove }: MoveListProps ) => {
    return (
        <section className="move-list-container">
            <h3>Moves</h3>

          <div className="move-list">
            {moves.map((move) => (
              <div className="move-row" key={move.move_number}>
                <span> {move.move_number}. </span>

                <button className={selectedMoveIndex === move.whiteIndex ? "move-button selected" : "move-button"} onClick={() => onSelectMove(move.whiteIndex)}>
                  {move.white}
                </button>

                {move.black && move.blackIndex !== null ? (
                  <button className={selectedMoveIndex === move.blackIndex ? "move-button selected" : "move-button"} onClick={() => onSelectMove(move.blackIndex as number)}>
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