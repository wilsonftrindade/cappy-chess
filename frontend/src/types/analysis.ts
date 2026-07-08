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
    classification: string | null;
}