import json
import time
from typing import Any, Literal

from fastapi import HTTPException
from psycopg_pool import ConnectionPool
from redis import Redis

from model.response import Response

class BaseQueries:
    __pg_pool: ConnectionPool
    __redis_client: Redis
    def __init__(self, pg_pool: ConnectionPool, redis_client: Redis) -> None:
        self.__pg_pool = pg_pool
        self.__redis_client = redis_client
    
    def get(
            self,
            type: Literal["one","all"],
            cachePrefix: str,
            query: str,
            role: Literal["Administrador", "Recepcionista", "Veterinario"],
            id: int | None = None
        ) -> Response:
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
            conn.execute(f"SET LOCAL ROLE {role}") # me sale todo en rojo pero funciona xd
            row = Any
            if type == "all":
                row = conn.execute(query).fetchall()
                if row.__len__() < 1:
                    raise HTTPException(status_code=404, detail="No se pudieron conseguir los usuarios")
            else:
                row = conn.execute(query).fetchone()
                if row is None:
                    raise HTTPException(status_code=404, detail="No se pudieron conseguir los usuarios")



        elapsed: float = (time.perf_counter()-t0) * 1000
        return {
            "cache_hit": False,
            "latency_ms": round(elapsed, 2),
            "data": row
        }