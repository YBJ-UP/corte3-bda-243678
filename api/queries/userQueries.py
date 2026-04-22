from typing import Literal

from psycopg_pool import ConnectionPool
from redis import Redis

from model.response import DeleteResponse, PatchResponse, Response
from queries.baseQueries import BaseQueries

class UserQueries(BaseQueries): # wrapper para ocultar los roles de los endpoints

    def __init__(self, pg_pool: ConnectionPool, redis_client: Redis, role: Literal['Administrador', 'Veterinario', 'Recepcionista']) -> None:
        super().__init__(pg_pool= pg_pool, redis_client= redis_client)
        self.ROLE: Literal['Administrador'] | Literal['Veterinario'] | Literal['Recepcionista'] = role

    def wipeAllCacheWrapper(self): # a canijo le di enter y me lo autocompletó
        return self._wipeAllCache(self.ROLE) # se vuelve a poner por que así no pide el rol desde los endpoints

    def getAll[T](self, model: type[T], cachePrefix: str, tableAlias: str, query: str) -> Response[T]:
        return self._get(
            type= "all",
            model= model,
            cachePrefix=cachePrefix,
            tableAlias= tableAlias,
            query= query,
            role= self.ROLE
        )

    def getOne[T](self, model: type[T], cachePrefix: str, id: int, tableAlias: str, query: str) -> Response[T]:
        return self._get(
            type= "one",
            model= model,
            cachePrefix= cachePrefix,
            tableAlias= tableAlias,
            query= query,
            role= self.ROLE,
            id= id
        )
    
    def patch[T](self, model: type[T], cachePrefix: str, id: int, data: T, tableName: str) -> PatchResponse[T]:
        return self._add_or_patch(
            isPatch= True,
            model= model,
            cachePrefix= cachePrefix,
            tableName= tableName,
            data= data,
            role=self.ROLE,
            id= id
        )
    
    def insert[T](self, model: type[T], cachePrefix: str, data: T, tableName: str) -> PatchResponse[T]:
        return self._add_or_patch(
            isPatch= False,
            model= model,
            cachePrefix= cachePrefix,
            tableName= tableName,
            data= data,
            role= self.ROLE
        )

    def delete(self, cachePrefix: str, id: int, tableName: str, query: str) -> DeleteResponse:
        return self._delete(
            cachePrefix= cachePrefix,
            tableName= tableName,
            query= query,
            role= self.ROLE,
            id= id
        )