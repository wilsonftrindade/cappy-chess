export type PlayerColor = "white" | "black";

export type DisplayMove = {
    move_number: number;
    white: string | null;
    black: string | null;
    whiteIndex: number;
    blackIndex: number | null;
};

export type ParseGameRequest = {
  pgn: string;
};

export type ParsedMove = {
  move_number: number;
  color: PlayerColor;
  move_san: string;
  move_uci: string;
  fen_before: string;
  fen_after: string;
};

export type ParsedGameResponse = {
  white: string;
  black: string;
  result: string | null;
  white_elo: number | null;
  black_elo: number | null;
  moves: ParsedMove[];
};