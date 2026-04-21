from model.owner import Owner
from model.response import DeleteResponse, PatchResponse, Response
from queries.baseQueries import BaseQueries


class AdminQueries(BaseQueries):
    ALL_OWNERS_QUERY = "SELECT * FROM duenos;"
    SELECT_OWNER_QUERY = "SELECT * FROM duenos WHERE id=%s;"
    DELETE_OWNER_QUERY = "DELETE FROM duenos WHERE id:%s"
    ROLE = "Administrador"

    OWNER_TABLE_NAME = "duenos"
    OWNER_TABLE_DESCRIPTION = "dueños"

    def wipeAllCacheWrapper(self): # a canijo le di enter y me lo autocompletó
        return self._wipeAllCache(self.ROLE)

    def getAllOwners(self, cachePrefix: str) -> Response[list[Owner]]:
        return self._get(
            type='all',
            model= list[Owner],
            cachePrefix=cachePrefix,
            tableName= self.OWNER_TABLE_DESCRIPTION,
            query= self.ALL_OWNERS_QUERY,
            role= self.ROLE
        )

    def getOwner(self, cachePrefix: str, id: int) -> Response[Owner]:
        return self._get(
            type="one",
            model= Owner,
            cachePrefix= cachePrefix,
            tableName= self.OWNER_TABLE_NAME,
            query= self.SELECT_OWNER_QUERY,
            role= self.ROLE,
            id= id
        )
    
    def patchOwner(self, cachePrefix: str, id: int, data: Owner) -> PatchResponse[Owner]:
        return self._add_or_patch(
            isPatch= True,
            model= Owner,
            cachePrefix= cachePrefix,
            tableName= self.OWNER_TABLE_NAME,
            data= data,
            role=self.ROLE,
            id= id
        )
    
    def insertOwner(self, cachePrefix: str, id: int, data: Owner) -> PatchResponse[Owner]:
        return self._add_or_patch(
            isPatch= False,
            model= Owner,
            cachePrefix= cachePrefix,
            tableName= self.OWNER_TABLE_NAME,
            data= data,
            role= self.ROLE,
            id= id
        )

    def deleteOwner(self, cachePrefix: str, id: int) -> DeleteResponse:
        return self._delete(
            model= Owner,
            cachePrefix= cachePrefix,
            tableName= self.OWNER_TABLE_NAME,
            query= self.DELETE_OWNER_QUERY,
            role= self.ROLE,
            id= id
        )