from psycopg_pool import ConnectionPool
from redis import Redis

from model.owner import OwnerBaseModel
from model.response import DeleteResponse, PatchResponse, Response
from queries.user import User

class AdminQueries(User):
    ROLE = "Administrador"

    def __init__(self, pg_pool: ConnectionPool, redis_client: Redis) -> None:
        super().__init__(pg_pool= pg_pool, redis_client= redis_client)

    def wipeAllCacheWrapper(self): # a canijo le di enter y me lo autocompletó
        return self._wipeAllCacheWrapper(self.ROLE)

    def getAll[T](self, model: type[T], cachePrefix: str, tableAlias: str, query: str) -> Response[T]:
        return self._getAll(
            model= model,
            cachePrefix=cachePrefix,
            tableAlias= tableAlias,
            query= query,
            role= self.ROLE
        )

    def getOne[T](self, model: type[T], cachePrefix: str, id: int, tableAlias: str, query: str) -> Response[T]:
        return self._getOne(
            model= model,
            cachePrefix= cachePrefix,
            tableAlias= tableAlias,
            query= query,
            role= self.ROLE,
            id= id
        )
    
    def patch[T](self, model: type[T], cachePrefix: str, id: int, data: T, tableName: str) -> PatchResponse[T]:
        return self._patch(
            model= model,
            cachePrefix= cachePrefix,
            tableName= tableName,
            data= data,
            role=self.ROLE,
            id= id
        )
    
    def insert(self, cachePrefix: str, data: OwnerBaseModel, tableName: str) -> PatchResponse[OwnerBaseModel]:
        return self._add_or_patch(
            isPatch= False,
            model= OwnerBaseModel,
            cachePrefix= cachePrefix,
            tableName= tableName,
            data= data,
            role= self.ROLE
        )

    def delete(self, cachePrefix: str, id: int, tableName: str, query: str) -> DeleteResponse:
        return self._deleteWrap(
            cachePrefix= cachePrefix,
            tableName= tableName,
            query= query,
            role= self.ROLE,
            id= id
        )