from dotenv import load_dotenv
import os
import redis  # Cambia aioredis a redis
from typing import Dict, Any
import asyncio

load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

# Función para obtener la conexión a Redis
def get_redis_connection():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True
    )

# Función para establecer datos de sesión
async def set_session_data(session_id: str, data: Dict[str, Any]):
    loop = asyncio.get_event_loop()
    redis_client = get_redis_connection()
    await loop.run_in_executor(None, redis_client.hmset, session_id, data)

# Función para obtener datos de sesión
async def get_session_data(session_id: str) -> Dict[str, Any]:
    loop = asyncio.get_event_loop()
    redis_client = get_redis_connection()
    data = await loop.run_in_executor(None, redis_client.hgetall, session_id)
    return data
