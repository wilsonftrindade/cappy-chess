import "./EvalGraph.css"
import { useState } from "react";
import type { ReviewedMove } from "../../types/analysis";

type EvalGraphProps = {
  reviewedMoves: ReviewedMove[];
  onSelectMove: (index: number) => void;
};

const formatEvaluation = (evaluationCp: number, mateIn: number | null) => {
  if (mateIn !== null) {
    return `M${Math.abs(mateIn)}`;
  }

  const pawns = evaluationCp / 100;

  return `${pawns >= 0 ? "+" : ""}${pawns.toFixed(1)}`;
};

const EvalGraph = ({ reviewedMoves, onSelectMove}: EvalGraphProps) => {
  const WIDTH = 800;
  const HEIGHT = 160;

  const [hoveredPointIndex, setHoveredPointIndex] = useState<number | null>(null);

  const points = [
    {
      moveIndex: null,
      whiteWinProbability: 0.5,
      evalCp: 0,
      mateIn: null,
    },

    ...reviewedMoves.map((move, index) => ({
        moveIndex: index,
        whiteWinProbability:
          (move.color === "white" ? move.win_probability_after : (move.win_probability_after ? 1 - move.win_probability_after : 0.5)) ?? 0.5,
        evalCp: (move.color === "white" ? move.eval_cp_after : (move.eval_cp_after ? move.eval_cp_after * -1 : 0)) ?? 0,
        mateIn: move.mate_in_after ? Math.abs(move.mate_in_after) : null
      })) 
  ];

  const coordinates = points.map((point, index) => {
    const normalized_y = 2 * point.whiteWinProbability - 1
    
    return {
      ...point,

      x:
        points.length === 1 
          ? WIDTH / 2 
          : (index / (points.length - 1)) * WIDTH,

      // weird SVG coordinate system grows downwards
      y:
        ((1 - normalized_y) / 2) * HEIGHT,
    };
  });

  const upperAreaPath = [
    `M 0 0`,
    `L ${WIDTH} 0`,

    ...coordinates
      .slice()
      .reverse()
      .map((point) => `L ${point.x} ${point.y}`),

    "Z",
  ].join(" ");

  const hoveredPoint = hoveredPointIndex !== null ? coordinates[hoveredPointIndex] : null;

  const hoveredEvaluation = hoveredPoint ? formatEvaluation(hoveredPoint.evalCp, hoveredPoint.mateIn) : null;

  const path = coordinates.map((point, index) => `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`).join(" ");

  const handleMouseMove = (event: React.MouseEvent<SVGSVGElement>) => {
    const bounds =
      event.currentTarget.getBoundingClientRect();

    const mouseX =
      event.clientX - bounds.left;

    const relativeX =
      mouseX / bounds.width;

    const index = Math.round(
      relativeX * (coordinates.length - 1)
    );

    const safeIndex = Math.max(
      0,
      Math.min(coordinates.length - 1, index)
    );

    setHoveredPointIndex(safeIndex);
  };

  const handleMouseLeave = () => {
    setHoveredPointIndex(null)
  }

  const handleClick = () => {
    if (hoveredPointIndex === null) {
      return;
    }

    const point =
      coordinates[hoveredPointIndex];

    if (point.moveIndex !== null) {
      onSelectMove(point.moveIndex);
    }
  };

  return (
    <div className="eval-graph">
      <svg
        viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
        preserveAspectRatio="none"
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        onClick={handleClick}
      >

         <path
          d={upperAreaPath}
          className="eval-graph-upper-area"
        />
        
        <line
          x1="0"
          y1={HEIGHT / 2}
          x2={WIDTH}
          y2={HEIGHT / 2}
          className="eval-graph-baseline"
        />

        <path
          d={path}
          className="eval-graph-line"
        />

        {hoveredPoint && (
          <>
            <line
              x1={hoveredPoint.x}
              y1={0}
              x2={hoveredPoint.x}
              y2={HEIGHT}
              className="eval-graph-hover-line"
            />

            <circle
              cx={hoveredPoint.x}
              cy={hoveredPoint.y}
              r={5}
              className="eval-graph-hover-point"
            />
          </>
        )}
      </svg>

      {hoveredPoint && (
        <div
          className="eval-graph-tooltip"
          style={{
            left: `${
              (hoveredPointIndex! /
                (coordinates.length - 1)) *
              100
            }%`,
          }}
        >
          {hoveredEvaluation}
        </div>
      )}

    </div>
  );
};

export default EvalGraph;
