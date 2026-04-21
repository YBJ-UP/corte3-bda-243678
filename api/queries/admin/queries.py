from model.owner import OwnerBaseModel
from model.response import DeleteResponse, PatchResponse, Response
from queries.baseQueries import BaseQueries

class AdminQueries(BaseQueries):
    ROLE = "Administrador"

    def wipeAllCacheWrapper(self): # a canijo le di enter y me lo autocompletó
        return self._wipeAllCache(self.ROLE)

    def getAll(self, cachePrefix: str, tableAlias: str, query: str) -> Response[list[OwnerBaseModel]]:
        return self._get(
            type='all',
            model= list[OwnerBaseModel],
            cachePrefix=cachePrefix,
            tableAlias= tableAlias,
            query= query,
            role= self.ROLE
        )

    def getOne(self, cachePrefix: str, id: int, tableAlias: str, query: str) -> Response[OwnerBaseModel]:
        return self._get(
            type="one",
            model= OwnerBaseModel,
            cachePrefix= cachePrefix,
            tableAlias= tableAlias,
            query= query,
            role= self.ROLE,
            id= id
        )
    
    def patch(self, cachePrefix: str, id: int, data: OwnerBaseModel, tableName: str) -> PatchResponse[OwnerBaseModel]:
        return self._add_or_patch(
            isPatch= True,
            model= OwnerBaseModel,
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
        return self._delete(
            model= OwnerBaseModel,
            cachePrefix= cachePrefix,
            tableName= tableName,
            query= query,
            role= self.ROLE,
            id= id
        )