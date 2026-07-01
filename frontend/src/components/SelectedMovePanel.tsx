const SelectedMovePanel = ( { move } ) => {
    return (
        <>
         <h3>Selected Move</h3>
                <p>
                  {move.move_number}. {move.color} {move.san}
                </p>
                <p> UCI: {move.uci}</p>
                <p>FEN before: {move.fen_before}</p>
                <p>FEN after: {move.fen_after}</p>
        </>
    );
};

export default SelectedMovePanel;