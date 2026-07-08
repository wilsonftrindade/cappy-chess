import type { AnalysisResponse, MoveReviewResponse } from "../types/analysis";

const API_BASE_URL = "http://localhost:8000";

export async function analyzeFen(fen: string, depth: number): Promise<AnalysisResponse> {
    const response = await fetch(`${API_BASE_URL}/api/analysis/analyze`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ fen, depth })
    });
    
    if (!response.ok) {
        throw new Error('Failed to analyze FEN');
    }

    const data = await response.json();
    return data;
}

export async function reviewMove(fenBefore: string, moveUci: string, depth: number): Promise<MoveReviewResponse> {
    const response = await fetch(`${API_BASE_URL}/api/analysis/move-review`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ fen_before: fenBefore , move_uci: moveUci, depth })
    });

    if (!response.ok) {
        throw new Error('Failed to review move');
    }

    const data = await response.json();
    return data;
}