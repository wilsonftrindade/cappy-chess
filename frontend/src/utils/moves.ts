import type { DisplayMove } from '../types/game'
import type { ReviewedMove } from '../types/analysis';

export function groupMoves(moves: ReviewedMove[]): DisplayMove[] {
    const displayMoves: DisplayMove[] = [];

    for (let i = 0; i < moves.length; i += 2) {
      const moveNumber = moves[i].move_number;
      const whiteMove = moves[i].move_san;
      const blackMove = (i + 1 < moves.length) ? moves[i + 1].move_san : null;

      const displayMove = {
        move_number: moveNumber,
        white: whiteMove,
        black: blackMove,
        whiteIndex: i,
        blackIndex: (i + 1 < moves.length) ? i + 1 : null
      };

      displayMoves.push(displayMove);
    }

    return displayMoves;
  }



  