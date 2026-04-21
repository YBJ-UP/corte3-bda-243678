import json
import time
from typing import Any, Literal

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
    
    def __add_to_cache(self, cache_key: str, data: Any) -> None:
        stringified_data: str = json.dumps(data, default= str)
        self.__redis_client.setex(cache_key, self.CACHE_TTL, stringified_data)
        return None
    
    def __wipe_cache(self, cache_key: str) -> None:
        self.__redis_client.delete(cache_key)
        return None
    
    def wipeAllCache(self, role: Literal["Administrador", "Recepcionista", "Veterinario"]):
        if role == "Administrador":
            self.__redis_client.flushdb()
            print("[FLUSH] caché vaciado", flush= True)
            return { "message":"Caché vaciado", "keys_remaining": self.__redis_client.dbsize() }
        else:
            raise HTTPException(403, { "message":"Sin permisos necesarios para vacíar caché." })

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

        self.__add_to_cache(cache_key=cache_key, data=row)

        elapsed: float = (time.perf_counter()-t0) * 1000
        return {
            "cache_hit": False,
            "latency_ms": round(elapsed, 2),
            "data": row
        }