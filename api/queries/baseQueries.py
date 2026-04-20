import json
import time
from typing import Literal

from fastapi import HTTPException
from psycopg_pool import ConnectionPool
from redis import Redis


class BaseQueries:
    __pg_pool: ConnectionPool
    __redis_client: Redis
    def __init__(self, pg_pool: ConnectionPool, redis_client: Redis) -> None:
        self.__pg_pool = pg_pool
        self.__redis_client = redis_client
    
    def get(self, type: Literal["one","all"], cachePrefix: str, query: str, id: int | None = None):
        t0: float = time.perf_counter()
        cache_key = f"{cachePrefix}"

        cached = self.__redis_client.get(cache_key)
        if cached is not None:
            elapsed: float = (time.perf_counter()-t0) * 1000
            print(f"[CACHE HIT] ({elapsed:.2f})", flush=True)
            return {
                "cache_hit": True,
                "latency_ms": round(elapsed, 2),
                "data": json.loads(cached)
            }
        with self.__pg_pool.connection() as conn:
            row = conn.execute(query).fetchall() # me sale todo en rojo pero funciona xd
        if row.__len__() < 1:
            raise HTTPException(status_code=404, detail="No se pudieron conseguir los usuarios")
        
        print(row)