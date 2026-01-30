import logging

from fastapi import FastAPI

from app.api import healthz, antifraud

import redis.asyncio as redis

from contextlib import asynccontextmanager

from app.config import get_settings

from app.redis_client import connect_redis, redis_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


redis_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    connected = await connect_redis()
    yield
app = FastAPI(lifespan = lifespan)

app.include_router(healthz.router)
app.include_router(antifraud.router)



import time

@app.get("/test-redis")
async def test_redis():
    from app.redis_client import redis_client, set, get

    test_key = "test_key"
    test_value = "test_value_" + str(time.time())

    results = {
        "redis_client_exists": redis_client is not None,
        "set_result": None,
        "get_result": None,
        "error": None
    }

    try:
        if redis_client:
            # Тест 1: SET
            results["set_result"] = await redis_client.set(test_key, test_value)

            # Тест 2: GET
            results["get_result"] = await redis_client.get(test_key)

            # Тест 3: Прямой через redis-cli
            results["direct_test"] = f"Run: redis-cli get '{test_key}'"
        else:
            results["error"] = "Redis client is None"

    except Exception as e:
        results["error"] = str(e)

    return results