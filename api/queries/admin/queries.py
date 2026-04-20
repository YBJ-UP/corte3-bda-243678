import json
import time

from fastapi import HTTPException
from psycopg_pool import ConnectionPool
from redis import Redis


class AdminQueries:
    __pg_pool: ConnectionPool
    __redis_client: Redis
    def __init__(self, pg_pool: ConnectionPool, redis_client: Redis) -> None:
        self.__pg_pool = pg_pool
        self.__redis_client = redis_client

    ALL_OWNERS_QUERY = "SELECT * FROM duenos;"

    def __FormQuery(self, Query: str) -> str:
        return f"BEGIN; SET LOCAL ROLE Administrador; {Query} COMMIT;"

    def getAllOwners(self, cachePrefix: str):
        print("hola")
        self.__FormQuery(self.ALL_OWNERS_QUERY)
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
            row = conn.execute(self.__FormQuery(self.ALL_OWNERS_QUERY)).fetchall() # me sale todo en rojo pero funciona xd
        if row.__len__() < 1:
            raise HTTPException(status_code=404, detail="No se pudieron conseguir los usuarios")
        
        print(row)