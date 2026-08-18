import "./EvalBar.css"

type EvalBarProps = {
  whiteWinProbability: number;
  evaluationCp: number;
  mateIn: number | null;
}

const EvalBar = ({ whiteWinProbability, evaluationCp, mateIn }: EvalBarProps) => {
  const whitePercentage = whiteWinProbability * 100;
  const blackPercentage = 100 - whitePercentage;
  console.log(whitePercentage)

  const evaluationLabel =
    mateIn !== null
      ? `M${Math.abs(mateIn)}`
      : `${(Math.abs(evaluationCp / 100)).toFixed(1)}`;

  const whiteWinning = whitePercentage >= 50;

  return (
    <div className="eval-bar">
      <div
        className="eval-bar-black"
        style={{ height: `${blackPercentage}%` }}
      />

      <span className= {whiteWinning ? "eval-bar-label eval-bar-label--white" : "eval-bar-label eval-bar-label--black"}>
        {evaluationLabel}
      </span>
    </div>
  );
};

export default EvalBar;