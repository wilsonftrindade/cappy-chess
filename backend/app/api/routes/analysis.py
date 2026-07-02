from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.engine import analyze_fen
from fastapi import APIRouter

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
def analyze_position(analysis_request: AnalysisRequest):
    return analyze_fen(analysis_request.fen, analysis_request.depth)