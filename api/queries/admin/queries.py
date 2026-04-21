from typing import Literal

from model.owner import Owner
from model.response import Response
from queries.baseQueries import BaseQueries


class AdminQueries(BaseQueries):
    ALL_OWNERS_QUERY = "SELECT * FROM duenos;"
    SELECT_OWNER_QUERY = "SELECT * FROM duenos WHERE id=%s;"
    DELETE_OWNER_QUERY = "DELETE FROM duenos WHERE id:%s"
    INSERT_OWNER_QUERY = "INSERT INTO duenos (nombre, telefono, email) VALUES %s, %s, %s"
    ROLE = "Administrador"

    OWNER_TABLE_NAME = "dueños"

    def __convert_to_tuples[T](self, model: type[T], data: T) -> tuple[tuple[str, ...], tuple[str, ...]]:
        return (tuple(data.keys()), tuple(data.values()))

    def wipeAllCacheWrapper(self): # a canijo le di enter y me lo autocompletó
        return self.wipeAllCache(self.ROLE)

    def getAllOwners(self, cachePrefix: str) -> Response[list[Owner]]:
        return self.get(
            type='all',
            model= list[Owner],
            cachePrefix=cachePrefix,
            tableName= self.OWNER_TABLE_NAME,
            query= self.ALL_OWNERS_QUERY,
            role= self.ROLE
        )

    def getOwner(self, cachePrefix: str, id: int) -> Response[Owner]:
        return self.get(
            type="one",
            model= Owner,
            cachePrefix= cachePrefix,
            tableName= self.OWNER_TABLE_NAME,
            query= self.SELECT_OWNER_QUERY,
            role= self.ROLE,
            id= id
        )
    
    def patchOwner(self, cachePrefix: str, id: int, data: Owner):
        keys, values = self.__convert_to_tuples( model=Owner, data=data)
        return self.patch(
            model= Owner,
            cachePrefix= cachePrefix,
            tableName= self.OWNER_TABLE_NAME,
            query= "",
            params= values,
            role= self.ROLE,
            id= id
        )
    
    def deleteOwner(self, cachePrefix: str, id: int):
        return self.delete(
            model= Owner,
            cachePrefix= cachePrefix,
            tableName= self.OWNER_TABLE_NAME,
            query= self.DELETE_OWNER_QUERY,
            role= self.ROLE,
            id= id
        )