from model.owner import Owner
from model.response import Response
from queries.baseQueries import BaseQueries


class AdminQueries(BaseQueries):
    ALL_OWNERS_QUERY = "SELECT * FROM duenos;"
    SELECT_OWNER_QUERY = "SELECT * FROM duenos WHERE id=%s;"
    DELETE_OWNER_QUERY = "DELETE FROM duenos WHERE id:%s"
    ROLE = "Administrador"

    OWNER_TABLE_NAME = "dueños"

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
    
    def patchOwner(self, cachePrefix: str, id: int):
        return self.patch(
            model= Owner,
            cachePrefix= cachePrefix,
            tableName= self.OWNER_TABLE_NAME,
            query= "",
            role= self.ROLE,
            id= id
        )