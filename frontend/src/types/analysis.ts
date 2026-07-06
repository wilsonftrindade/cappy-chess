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