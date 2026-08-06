from rq import Queue
from app.core.redis_client import redis_client

review_queue = Queue("game-reviews", connection=redis_client)