import redis.asyncio as redis
import logging
from app.config import get_settings
logger = logging.getLogger(__name__)
import os

redis_client = None


async def connect_redis():
    global redis_client
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    try:
        redis_client = redis.Redis(host=redis_host,
                                port=redis_port,
                                    decode_responses=True)

        await redis_client.ping()
        logger.info("redis good")
        return True
    except Exception as e:
        logger.error(f"redis bad: {e}")
        redis_client = None
        return False

async def get(key):
    if redis_client:
        try:
            return await redis_client.get(key)
        except Exception as e:
            logger.error(f"eroor while get: {e}")
            return None
    return None

async def set(key, value):
    if redis_client:
        try:
            result = await redis_client.set(key, value)
            return result
        except Exception as e:
            logger.error(f"error while set: {e}")
            return None
    return None