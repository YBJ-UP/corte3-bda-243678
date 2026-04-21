import json
import time
from typing import Literal

from fastapi import HTTPException
from psycopg_pool import ConnectionPool
from redis import Redis

from model.characterValidator import Validator
from model.response import Response

class BaseQueries:
    __pg_pool: ConnectionPool
    __redis_client: Redis
    validator: Validator
    def __init__(self, pg_pool: ConnectionPool, redis_client: Redis, validator: Validator) -> None:
        self.__pg_pool = pg_pool
        self.__redis_client = redis_client
        self.validator = validator

    CACHE_TTL = 300

    def __get_from_cache(self, cache_key: str):
        cached = self.__redis_client.get(cache_key)
        if cached:
            return json.dumps(cached)
        return None
    
    def __add_to_cahce(self) -> None:
        return None
    
    def __wipe_cache(self) -> None:
        return None

    def get[T](
            self,
            model: type[T],
            type: Literal["one","all"],
            cachePrefix: str,
            query: str,
            role: Literal["Administrador", "Recepcionista", "Veterinario"],
            id: int | None = None
        ) -> Response[T]:
        t0: float = time.perf_counter()
        cache_key: str = f"{cachePrefix}{id}" if id is not None else cachePrefix

        cached = self.__get_from_cache(cache_key)
        if cached is not None:
            elapsed: float = (time.perf_counter()-t0) * 1000
            print(f"[CACHE HIT] ({elapsed:.2f})", flush=True)
            return {
                "cache_hit": True,
                "latency_ms": round(elapsed, 2),
                "data": json.loads(cached)
            }

        row:T
        with self.__pg_pool.connection() as conn:
            conn.execute(f"SET LOCAL ROLE {role}") # me sale todo en rojo pero funciona xd
            if type == "all":
                row: T = conn.execute(query).fetchall() # no se usa el "" pero si no lo pongo no me da el tipado el ide
            else:
                assert id is not None
                row: T = conn.execute(query, (id,)).fetchone()
                if row is None:
                    raise HTTPException(status_code=404, detail="No se encontró el usuario")

        # aqui irá el cache pero ahorita1

        elapsed: float = (time.perf_counter()-t0) * 1000
        return {
            "cache_hit": False,
            "latency_ms": round(elapsed, 2),
            "data": row
        }