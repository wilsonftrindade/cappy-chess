type AnalysisPanelProps = {
    analysis: AnalysisResponse | null;
    isAnalyzing: boolean;
    analysisError: string | null;
    onAnalyzeMove: () => void;
};

function formatEvaluation(evaluation: number | null, mate_in: number | null): string {

    if (mate_in !== null) {
        return `Mate in ${mate_in}`;
    }

    if (evaluation === null) {
        return "Evaluation not available";
    }
    
    const eval_score = evaluation / 100; 

    if (eval_score > 0) {
        return `+${eval_score.toFixed(2)}`;
    }

    return `${eval_score.toFixed(2)}`;
};

const AnalysisPanel = ( { analysis, isAnalyzing, analysisError, onAnalyzeMove  }: AnalysisPanelProps ) => {
    return (
        <section className="analysis-panel">
            <h3> Engine Analysis</h3>

            <button onClick={onAnalyzeMove} disabled={isAnalyzing}>
                {isAnalyzing ? "Analyzing..." : "Analyze Move"}
            </button>

            {analysisError ? (
                <p className="error-message">{analysisError}</p>
            ) : null}

            {analysis ? (
                <div className="analysis-results">
                    <p>
                        <strong>Best Move: </strong> {analysis.best_move_san}
                    </p>

                    <p>
                        <strong> Evaluation: </strong> {formatEvaluation(analysis.evaluation_cp, analysis.mate_in)}
                    </p>

                    <p>
                        <strong> Best Move UCI: </strong> {analysis.best_move_uci}
                    </p>

                    <p>
                        <strong>Line:</strong>{" "}
                        {analysis.main_variation.length > 0
                        ? analysis.main_variation.join(" ")
                        : "No line available"}
                    </p>
                </div>
            ) : null}
        </section>)
};

export default AnalysisPanel;