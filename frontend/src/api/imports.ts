import type { ImportedGamesResponse } from "../types/imports";
import type { GameSource } from "../types/analysis";

const API_BASE_URL = "http://localhost:8000";

const sourcePath = {
  manual: "manual",
  chess_com: "chess-com",
  lichess: "lichess"
} 

export async function getImportedGames(source: GameSource, username: string, limit: number, signal?: AbortSignal): Promise<ImportedGamesResponse> {
  const response = await fetch(`${API_BASE_URL}/api/imports/${sourcePath[source]}/${encodeURIComponent(username)}/games?limit=${limit}`, { signal }); 

  if (!response.ok) {
    const result = await response.json().catch(() => null);
    throw new Error(result?.detail ?? 'Failed to fetch imported games');
  }

  const data = await response.json();
  return data;
}