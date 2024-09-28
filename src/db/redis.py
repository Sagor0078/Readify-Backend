from redis.asyncio import Redis
from src.config import Config

JTI_EXPIRY = 3600

# Initialize Redis connection using redis-py
token_blocklist = Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)

async def add_jti_to_blocklist(jti: str) -> None:
    # Using 'set' with expiration
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)

async def token_in_blocklist(jti: str) -> bool:
    # Check if JTI is in the blocklist
    result = await token_blocklist.get(jti)
    return result is not None
