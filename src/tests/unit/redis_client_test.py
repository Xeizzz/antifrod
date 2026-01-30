import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from app.redis_client import connect_redis, get, set, redis_client

@pytest.mark.asyncio
async def test_connection_reddis():
    with patch('redis.asyncio.Redis') as mock_redis_cl:
        mock_instance = AsyncMock
        mock_instance.ping = AsyncMock(return_value = True)
        mock_redis_cl.return_value = mock_instance
        result = await connect_redis()
        assert result is True
        assert redis_client is None

@pytest.mark.asyncio
async def test_get_set():
    with patch('redis.asyncio.Redis') as mock_redis:
        mock_instance = AsyncMock()
        mock_instance.get = AsyncMock(return_value = '{"test": "data"}')
        mock_instance.set = AsyncMock(return_value = True)
        mock_redis.return_value = mock_instance

        await connect_redis()

        set_result = await set("test_key", "test_value")
        assert set_result is True

        get_result = await get("test_key")
        assert get_result == '{"test": "data"}'