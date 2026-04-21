from model.owner import Owner
from model.response import Response
from queries.baseQueries import BaseQueries


class AdminQueries(BaseQueries):
    ALL_OWNERS_QUERY = "SELECT * FROM duenos;"
    SELECT_OWNER_QUERY = "SELECT * FROM duenos WHERE id=%s;"
    ROLE = "Administrador"

    def wipeAllCacheWrapper(self): # a canijo le di enter y me lo autocompletó
        return self.wipeAllCache(self.ROLE)

    def getAllOwners(self, cachePrefix: str) -> Response[list[Owner]]:
        return self.get(
            type='all',
            model= list[Owner],
            cachePrefix=cachePrefix,
            query= self.ALL_OWNERS_QUERY,
            role= self.ROLE
        )

    def getOwner(self, cachePrefix: str, id: int) -> Response[Owner]:
        return self.get(
            type="one",
            model= Owner,
            cachePrefix= cachePrefix,
            query= self.SELECT_OWNER_QUERY,
            role= self.ROLE,
            id= id
        )