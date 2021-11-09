from typing import Tuple
import aioredis


class RedisBackend:
    __redis = None

    async def connect(self, url):
        self.__redis = aioredis.from_url(url,
                                         encoding="utf8", decode_responses=True)

    async def get_with_ttl(self, key: str) -> Tuple[int, str]:
        async with self.__redis.pipeline(transaction=True) as pipe:
            return await (pipe.ttl(key).get(key).execute())

    async def get(self, key) -> str:
        return await self.__redis.get(key)

    async def set(self, key: str, value: str, expire: int = None):
        return await self.__redis.set(key, value, ex=expire)

    async def clear(self, namespace: str = None, key: str = None) -> int:
        if namespace:
            lua = f"for i, name in ipairs(redis.call('KEYS', '{namespace}:*')) do redis.call('DEL', name); end"
            return await self.__redis.eval(lua, numkeys=0)
        elif key:
            return await self.__redis.delete(key)


redis_backend = RedisBackend()
