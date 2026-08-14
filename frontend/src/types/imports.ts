import type { GameSource } from "./analysis";

export type ImportedGame = {
  external_id: string;
  source: GameSource;
  pgn: string;
  white: string;
  black: string;
  white_elo: number | null;
  black_elo: number | null;
  result: string;
  played_at: string;
  time_class: string;
}

export type ImportedGamesResponse = {
  username: string;
  source: GameSource;
  games: ImportedGame[];
}
