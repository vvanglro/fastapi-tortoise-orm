# https://github.com/long2ice/fastapi-cache/blob/master/fastapi_cache/backends/inmemory.py
import time
from asyncio import Lock
from dataclasses import dataclass
from multiprocessing import Manager
from typing import Optional
from typing import Tuple


@dataclass
class Value:
    data: str
    ttl_ts: int


class InMemoryBackend:
    _store = Manager().dict()
    _lock = Lock()

    @property
    def _now(self) -> int:
        return int(time.time())

    def _get(self, key: str):
        v = self._store.get(key)
        if v:
            if v[1] < self._now:
                del self._store[key]
            else:
                return v

    async def get_with_ttl(self, key: str) -> Tuple[int, Optional[str]]:
        async with self._lock:
            v = self._get(key)
            if v:
                return v.ttl_ts - self._now, v.data
            return 0, None

    async def get(self, key: str) -> str:
        async with self._lock:
            v = self._get(key)
            if v:
                return v[0]

    async def set(self, key: str, value: str, expire: int = None):
        async with self._lock:
            self._store[key] = (value, self._now + expire or 0)
            return

    async def clear(self, namespace: str = None, key: str = None) -> int:
        count = 0
        if namespace:
            keys = list(self._store.keys())
            for key in keys:
                if key.startswith(namespace):
                    del self._store[key]
                    count += 1
        elif key:
            del self._store[key]
            count += 1
        return count


cache = InMemoryBackend()

#
# def test(key):
#     r = loop.run_until_complete(cache.set(key, '1', 10))
#     print(r)
#     # await cache.set(key,"1", 10)
#     # await asyncio.sleep(3)
#
#
# def test1(key):
#     r = loop.run_until_complete(cache.get(key))
#     print(r)
#
#
# def main():
#     process_list = []
#
#     worker_proc = multiprocessing.Process(
#         target=test,
#         args=('q',),
#     )
#     worker_proc.start()
#     process_list.append(worker_proc)
#     worker_proc1 = multiprocessing.Process(
#         target=test1,
#         args=('q',),
#     )
#     worker_proc1.start()
#     process_list.append(worker_proc1)
#
#     for process in process_list:
#         process.join()
#
#
# if __name__ == '__main__':
#     import multiprocessing
#     import asyncio
#     loop = asyncio.get_event_loop()
#     main()
