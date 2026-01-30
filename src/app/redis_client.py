import redis.asyncio as redis
import logging
from app.config import get_settings
logger = logging.getLogger(__name__)

redis_client = None


async def connect_redis():
    global redis_client
    settings = get_settings()
    redis_client = redis.Redis(host=settings.redis_host,
                               port=settings.redis_port,
                                decode_responses=True)


async def get(key):
    if redis_client:
        return await redis_client.get(key)
    return None

async def set(key, value):
    if redis_client:
        await redis_client.set(key, value)