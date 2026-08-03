import type { ReviewJob } from '../../types/reviewJob'
import './AnalysisOverlay.css'

type AnalysisOverlayProps = {
    reviewJob: ReviewJob | null;
    isVisible: boolean;
};

const AnalysisOverlay = ({ reviewJob, isVisible }: AnalysisOverlayProps) => {
  if (!isVisible) {
    return null;
  }

  const completedPlies = reviewJob?.completed_plies ?? 0;
  const totalPlies = reviewJob?.total_plies ?? null;

  const progressPercentage = totalPlies ? Math.round((completedPlies / totalPlies) * 100) : null;

  let statusMessage = "Creating review job...";

  if (reviewJob?.status === "queued") {
    statusMessage = "Starting analysis...";
  }

  if (reviewJob?.status === "running") {
    statusMessage = totalPlies !== null ? `Analyzed ${completedPlies} of ${totalPlies} moves` : "Preparing analysis...";
  }

  if (reviewJob?.status === "completed") {
    statusMessage = "Finalizing game review...";
  }

  if (reviewJob?.status === "failed") {
    reviewJob.error ? statusMessage = `Error: ${reviewJob.error}` : statusMessage = "Game review job failed";
  }

  return (
    <div className="analysis-overlay">
      <section
        className="analysis-overlay-card"
        role="status"
        aria-live="polite"
        aria-busy="true"
      >
        <h2>Analyzing game</h2>

        <p>{statusMessage}</p>

        <progress
          className="analysis-progress"
          max={100}
          value={progressPercentage ?? undefined}
        />

        {progressPercentage !== null ? (
          <strong className="analysis-progress-label">
            {progressPercentage}%
          </strong>
        ) : null}
      </section>
    </div>
  );
}

export default AnalysisOverlay;