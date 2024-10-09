

from redis import asyncio as aioredis
from src.config import Config

JTI_EXPIRY = 3600
REDIS_URL = "redis://localhost:6379/0"

token_blocklist = aioredis.from_url(REDIS_URL)
  


async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti:str) -> bool:
   jti =  await token_blocklist.get(jti)

   return jti is not None