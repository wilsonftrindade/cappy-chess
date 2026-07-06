import type { AnalysisResponse } from "../types/analysis";

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