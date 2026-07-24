export type AnalysisRequest = {
    fen: string;
    depth: number;
}

export type AnalysisResponse = {
    fen: string;
    best_move_uci: string | null;
    best_move_san: string | null;
    evaluation_cp: number | null;
    mate_in: number | null;
    main_variation: string[] | null;
}

export type MoveReviewRequest = {
    fen_before: string;
    move_uci: string;
    depth: number;
}

export type MoveReviewResponse = {
    fen_before: string;
    move_uci: string;
    move_san: string | null;
    best_move_uci: string | null;
    best_move_san: string | null;
    eval_cp_before: number | null;
    eval_cp_after: number | null;
    eval_cp_loss: number | null;
    mate_in_before: number | null;
    mate_in_after: number | null;
    win_probability_before: number | null;
    win_probability_after: number | null;
    win_probability_loss: number | null;
    classification: string | null;
    move_accuracy: number | null;
}

export type GameReviewRequest = {
    pgn: string;
    depth: number;
}

export type ReviewedMove = {
    fen_before: string;
    move_uci: string;
    move_san: string | null;
    best_move_uci: string | null;
    best_move_san: string | null;
    eval_cp_before: number | null;
    eval_cp_after: number | null;
    eval_cp_loss: number | null;
    mate_in_before: number | null;
    mate_in_after: number | null;
    win_probability_before: number | null;
    win_probability_after: number | null;
    win_probability_loss: number | null;
    classification: string | null;
    move_accuracy: number | null;
    move_number: number
    color: string
    fen_after: string
}

export type PlayerReviewSummary = {
    move_count: number
    accuracy: number | null
    classification_counts: Record<string, number>;
}

export type GameReviewResponse = {
    white: string
    black: string
    result: string
    white_elo: number | null
    black_elo: number | null
    reviewed_moves: ReviewedMove[]
    white_summary: PlayerReviewSummary 
    black_summary: PlayerReviewSummary 
}

