from redis.asyncio import Redis
from src.config import Config

JTI_EXPIRY = 3600

# Initialize Redis connection using redis-py
token_blocklist = Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)

async def add_jti_to_blocklist(jti: str) -> None:
    try:
        # Using 'set' with expiration
        await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)
    except Exception as e:
        # Log or handle the Redis connection error
        print(f"Failed to add JTI to blocklist: {e}")
        raise e

async def token_in_blocklist(jti: str) -> bool:
    try:
        # Check if JTI is in the blocklist
        result = await token_blocklist.get(jti)
        return result is not None
    except Exception as e:
        # Log or handle the Redis connection error
        print(f"Failed to check if JTI is in blocklist: {e}")
        raise e
