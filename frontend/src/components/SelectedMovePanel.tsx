import type { ParsedMove } from "../types/game";

type SelectedMovePanelProps = {
    move: ParsedMove;
};


const SelectedMovePanel = ( { move }: SelectedMovePanelProps ) => {
    return (
        <section className="selected-move-panel">
         <h3>Selected Move</h3>
            <div className="selected-move-summary">
                <p>
                  {move.move_number}. {move.color} {move.san}
                </p>
                <p> UCI: {move.uci}</p>
            </div>   
        
            <div className="fen-block">
                <span className="fen-label">FEN before</span>
                <code>{move.fen_before}</code>
            </div>

            <div className="fen-block">
                <span className="fen-label">FEN after</span>
                <code>{move.fen_after}</code>
            </div>

        </section>
    );
};

export default SelectedMovePanel;