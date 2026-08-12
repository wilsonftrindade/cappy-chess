import type { GameReviewResponse } from "./analysis";

export type ReviewJobStatus = "queued" | "running" | "completed" | "failed";

export type ReviewJobCreatedResponse = {
    job_id: string;
    status: ReviewJobStatus;
}

export type ReviewJob = {
    job_id: string;
    status: ReviewJobStatus;
    completed_plies: number;
    total_plies: number | null;
    result : GameReviewResponse | null;
    error: string | null;
}

export type StoredReviewResponse= {
    id: string;
    game_id: string;
    depth: number;
    status: ReviewJobStatus;
    result: GameReviewResponse | null;
    error: string | null;
    created_at: string;
    completed_at: string | null;
}

