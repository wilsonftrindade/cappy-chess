import type { ParsedGameResponse } from "../types/game";

const API_BASE_URL = "http://localhost:8000";

export async function parseGame(pgn: string): Promise<ParsedGameResponse> {
    const response = await fetch(`${API_BASE_URL}/api/games/parse`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ pgn }),
    });

    if (!response.ok) {
        throw new Error(`Failed to parse game`);
    }

    const data = await response.json();
    return data;
}