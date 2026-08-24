import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://chess_coach:chess_coach_dev@localhost:5433/chess_coach")
LICHESS_API_TOKEN = os.getenv("LICHESS_API_TOKEN")