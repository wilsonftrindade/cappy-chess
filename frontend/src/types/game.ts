export type PlayerColor = "white" | "black";

export type ParseGameRequest = {
  pgn: string;
};

export type ParsedMove = {
  move_number: number;
  color: PlayerColor;
  san: string;
  uci: string;
  fen_before: string;
  fen_after: string;
};

export type ParsedGameResponse = {
  white: string | null;
  black: string | null;
  result: string | null;
  white_elo: number | null;
  black_elo: number | null;
  moves: ParsedMove[];
};