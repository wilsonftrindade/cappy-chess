import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
LICHESS_API_TOKEN = os.getenv("LICHESS_API_TOKEN")