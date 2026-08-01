from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, games, analysis, review_jobs


app = FastAPI(title="Chess Coach API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(games.router, prefix="/api/games")
app.include_router(analysis.router, prefix="/api/analysis")
app.include_router(review_jobs.router, prefix="/api/analysis")