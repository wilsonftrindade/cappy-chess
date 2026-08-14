import type { ReviewJobCreatedResponse, ReviewJob, StoredReviewResponse } from "../types/reviewJob";
import type { GameSource } from "../types/analysis";


const API_BASE_URL = "http://localhost:8000";

export async function createReviewJob(pgn: string, depth: number, source: GameSource, external_id: string | null, signal?: AbortSignal): Promise<ReviewJobCreatedResponse> {
    const response = await fetch(`${API_BASE_URL}/api/analysis/review-jobs`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ pgn, depth, source, external_id}),
        signal
    });

    if (!response.ok) {
        throw new Error('Failed to review game');
    }

    const data = await response.json();
    return data;

}

export async function getReviewJob(jobId: string, signal?: AbortSignal): Promise<ReviewJob> {
    const response = await fetch(`${API_BASE_URL}/api/analysis/review-jobs/${jobId}`, { signal });

    if (!response.ok) {
        throw new Error('Failed to fetch review job');
    }

    const data = await response.json();
    return data;
}

export async function getPersistedReview(jobId: string, signal?: AbortSignal): Promise<StoredReviewResponse> {
    const response = await fetch(`${API_BASE_URL}/api/analysis/reviews/${jobId}`, { signal });

    if (!response.ok) {
        throw new Error('Failed to fetch review');
    }

    const data = await response.json();
    return data;
}
