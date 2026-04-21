import json
import time
from typing import Any, Literal

from fastapi import HTTPException
from psycopg_pool import ConnectionPool
from redis import Redis

from model.response import DeleteResponse, PatchResponse, Response

class BaseQueries:
    __pg_pool: ConnectionPool
    __redis_client: Redis
    def __init__(self, pg_pool: ConnectionPool, redis_client: Redis) -> None:
        self.__pg_pool = pg_pool
        self.__redis_client = redis_client

    CACHE_TTL = 300

    def __get_from_cache(self, cache_key: str):
        cached = self.__redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        return None
    
    def __add_to_cache(self, cache_key: str, data: Any) -> None:
        stringified_data = json.dumps(data, default=str)
        self.__redis_client.setex(cache_key, self.CACHE_TTL, stringified_data)
        return None
    
    def __wipe_cache(self, cache_key: str) -> None:
        self.__redis_client.delete(cache_key)
        return None
    
    def __convert_to_tuples[T](self, model: type[T], data: T) -> tuple[tuple[str, ...], tuple[str, ...]]:
        return (tuple(data.model_dump(exclude_unset=True).keys()), tuple(data.model_dump(exclude_unset=True).values()))
    
    def __prepare_clauses(self, keys: tuple[str,...]) -> list[str]:
        clauses: list[str] = []
        for key in keys:
            clauses.append(f"{key}= %s")
        return clauses

    def __prepare_query[T](self, model: type[T], isPatch: bool, data: T, tableName: str, id: int | None = None) -> tuple[str, tuple[str,...]]:
        keys, values = self.__convert_to_tuples(model= model, data= data)

        clauses: list[str] = self.__prepare_clauses(keys)
        
        valuesList: list[str] = list(values)
        preparedQuery: str = ''
        if isPatch:
            assert id is not None
            preparedQuery: str = f"UPDATE {tableName} SET {", ".join(clauses)} WHERE ID = %s RETURNING *;"
            valuesList.append(str(id))
        else:
            preparedQuery: str = f"INSERT INTO {tableName} ({", ".join(keys)}) VALUES {", ".join(["%s"] * len(keys))}; RETURNING *"
        

        return preparedQuery, tuple(valuesList)
    
    def _add_or_patch[T](self, model: type[T], isPatch: bool, cachePrefix: str, tableName: str, data: T, role: Literal['Administrador', 'Recepcionista', 'Veterinario'], id: int | None = None) -> PatchResponse[T]:
        query, values = self.__prepare_query(model= model, isPatch= True, data= data, id= id, tableName= tableName)
        return self.__patch_insert(
            model= model,
            isPatch= isPatch,
            cachePrefix= cachePrefix,
            tableName= tableName,
            query= query,
            params= values,
            role= role,
            id= id
        )

    def _wipeAllCache(self, role: Literal["Administrador", "Recepcionista", "Veterinario"]):
        if role == "Administrador":
            self.__redis_client.flushdb()
            print("[FLUSH] caché vaciado", flush= True)
            return { "message":"Caché vaciado", "keys_remaining": self.__redis_client.dbsize() }
        else:
            raise HTTPException(403, { "message":"Sin permisos necesarios para vacíar caché." })

    def _get[T](
            self,
            model: type[T],
            type: Literal["one","all"],
            cachePrefix: str,
            query: str,
            tableAlias: str,
            role: Literal["Administrador", "Recepcionista", "Veterinario"],
            id: int | None = None
        ) -> Response[T]:
        t0: float = time.perf_counter()
        cache_key: str = f"{cachePrefix}:{id}" if id is not None else cachePrefix

        cached = self.__get_from_cache(cache_key)
        if cached is not None:
            elapsed: float = (time.perf_counter()-t0) * 1000
            print(f"[CACHE HIT] ({elapsed:.2f})", flush=True)
            return {
                "cache_hit": True,
                "latency_ms": round(elapsed, 2),
                "data": cached
            }

        row:T
        with self.__pg_pool.connection() as conn:
            conn.execute(f"SET LOCAL ROLE {role}") # me sale todo en rojo pero funciona xd
            if type == "all":
                row: T = conn.execute(query).fetchall()
            else:
                assert id is not None
                row: T = conn.execute(query, (id,)).fetchone()
                if row is None:
                    raise HTTPException(status_code=404, detail=f"No se encontró el {tableAlias} buscado")

        self.__add_to_cache(cache_key=cache_key, data=row)

        elapsed: float = (time.perf_counter()-t0) * 1000
        return {
            "cache_hit": False,
            "latency_ms": round(elapsed, 2),
            "data": row
        }
    
    def __patch_insert[T](
            self,
            isPatch: bool,
            model: type[T],
            cachePrefix: str,
            tableName: str,
            query: str,
            params: tuple[str, ...],
            role: Literal["Administrador", "Recepcionista", "Veterinario"],
            id: int | None = None
    ) -> PatchResponse[T]:
        t0: float = time.perf_counter()

        result: T
        with self.__pg_pool.connection() as conn:
            conn.execute(f"SET LOCAL ROLE {role}")
            result: T = conn.execute(query, params).fetchone()
            conn.commit()

        if result is None:
            raise HTTPException(404, f"No se encontró el {tableName} buscado")
        
        if isPatch:
            assert id is not None
            cache_key: str = f"{cachePrefix}:{id}"
            self.__wipe_cache(cache_key)
        else:
            self.__wipe_cache(cachePrefix)
        
        elapsed: float = (time.perf_counter() - t0) * 1000
        return {
            "message": "Dato actualizado con éxito.",
            "cache_invalidated":  True,
            "latency_ms": round(elapsed, 2),
            "updated_data": result
        }
    
    def _delete(
            self,
            cachePrefix: str,
            tableName: str,
            query: str,
            role: Literal["Administrador", "Recepcionista", "Veterinario"],
            id: int
    ) -> DeleteResponse:
        t0: float = time.perf_counter()

        result: Any
        with self.__pg_pool.connection() as conn:
            conn.execute(f"SET LOCAL ROLE {role}")
            result: Any = conn.execute(query, (id,)).fetchone()
            conn.commit()

        if result is None:
            raise HTTPException(404, f"No se encontró el {tableName} buscado")
        
        cache_key: str = f"{cachePrefix}:{id}"
        self.__wipe_cache(cache_key)
        
        elapsed: float = (time.perf_counter() - t0) * 1000
        return {
            "message": "Dato eliminado con éxito.",
            "cache_invalidated":  True,
            "latency_ms": round(elapsed, 2)
        }