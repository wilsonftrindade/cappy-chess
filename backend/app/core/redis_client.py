from redis import Redis
from rq import Queue
from app.core.config import REDIS_URL

redis_client = Redis.from_url(REDIS_URL)
review_queue = Queue("game-reviews", connection=redis_client)