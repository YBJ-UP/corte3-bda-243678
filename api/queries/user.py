from typing import Literal

from model.response import DeleteResponse, PatchResponse, Response
from queries.baseQueries import BaseQueries

class User(BaseQueries):
    def _wipeAllCacheWrapper(self, role: Literal["Administrador", "Veterinario", "Recepcionista"]): # a canijo le di enter y me lo autocompletó
        return self._wipeAllCache(role)

    def _getAll[T](self, model: type[T], cachePrefix: str, tableAlias: str, query: str, role: Literal["Administrador", "Veterinario", "Recepcionista"]) -> Response[T]:
        return self._get(
            type='all',
            model= model,
            cachePrefix=cachePrefix,
            tableAlias= tableAlias,
            query= query,
            role= role
        )

    def _getOne[T](self, model: type[T], cachePrefix: str, id: int, tableAlias: str, query: str, role: Literal["Administrador", "Veterinario", "Recepcionista"]) -> Response[T]:
        return self._get(
            type="one",
            model= model,
            cachePrefix= cachePrefix,
            tableAlias= tableAlias,
            query= query,
            role= role,
            id= id
        )
    
    def _patch[T](self, model: type[T], cachePrefix: str, id: int, data: T, tableName: str, role: Literal["Administrador", "Veterinario", "Recepcionista"]) -> PatchResponse[T]:
        return self._add_or_patch(
            isPatch= True,
            model= model,
            cachePrefix= cachePrefix,
            tableName= tableName,
            data= data,
            role= role,
            id= id
        )
    
    def _insert[T](self, model: type[T], cachePrefix: str, data: T, tableName: str, role: Literal["Administrador", "Veterinario", "Recepcionista"]) -> PatchResponse[T]:
        return self._add_or_patch(
            isPatch= False,
            model= model,
            cachePrefix= cachePrefix,
            tableName= tableName,
            data= data,
            role= role
        )

    def _deleteWrap(self, cachePrefix: str, id: int, tableName: str, query: str, role: Literal["Administrador", "Veterinario", "Recepcionista"]) -> DeleteResponse:
        return self._delete(
            cachePrefix= cachePrefix,
            tableName= tableName,
            query= query,
            role= role,
            id= id
        )