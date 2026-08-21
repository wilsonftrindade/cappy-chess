import bestMoveIcon from "../assets/move-classifications/best-move.png";
import blunderIcon from "../assets/move-classifications/blunder.png";
import excellentMoveIcon from "../assets/move-classifications/excellent-move.png";
import goodMoveIcon from "../assets/move-classifications/good-move.png";
import inaccuracyIcon from "../assets/move-classifications/inaccuracy.png";
import mistakeIcon from "../assets/move-classifications/mistake.png";

type ClassificationDetails = {
  icon: string;
  slug: string;
};

const CLASSIFICATION_DETAILS: Record<string, ClassificationDetails> = {
  Best: {
    icon: bestMoveIcon,
    slug: "best",
  },
  Excellent: {
    icon: excellentMoveIcon,
    slug: "excellent",
  },
  Good: {
    icon: goodMoveIcon,
    slug: "good",
  },
  Inaccuracy: {
    icon: inaccuracyIcon,
    slug: "inaccuracy",
  },
  Mistake: {
    icon: mistakeIcon,
    slug: "mistake",
  },
  Blunder: {
    icon: blunderIcon,
    slug: "blunder",
  },
};

export function getClassificationDetails(
  classification: string | null | undefined,
): ClassificationDetails | null {
  if (!classification) {
    return null;
  }

  return CLASSIFICATION_DETAILS[classification] ?? null;
}
