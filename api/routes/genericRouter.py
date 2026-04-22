from typing import Type

from fastapi import APIRouter

from lib.constants import tabla
from model.response import DeleteResponse, PatchResponse, Response
from queries.userQueries import UserQueries

def create_routes[T_read, T_add, T_patch](
        user: UserQueries,
        table: tabla,
        path: str,
        read: Type[T_read],
        add: Type[T_add],
        patch: Type[T_patch]
) -> APIRouter:
    router = APIRouter(prefix= path)

    @router.get("", response_model=Response[list[read]])
    def get_All() -> Response[list[T_read]]:
        return user.getAll(
            model= list[T_read],
            cachePrefix= table.CACHE_PREFIX,
            tableAlias= table.ALIAS,
            query= table.SELECT_ALL_QUERY
        )
    
    @router.get("/{id}", response_model=Response[read])
    def get_One(id: int) -> Response[T_read]:
        return user.getOne(
            model= read,
            cachePrefix= table.CACHE_PREFIX,
            id= id,
            tableAlias= table.ALIAS,
            query= table.SELECT_ONE_QUERY
        )
    
    @router.post("", response_model=Response[add])
    def post(data: add) -> PatchResponse[T_add]:
        return user.insert(
            model= add,
            cachePrefix= table.CACHE_PREFIX, 
            data= data,
            tableName= table.NAME
        )
    
    @router.patch("/{id}", response_model=Response[patch])
    def update(id: int, data: patch) -> PatchResponse[T_patch]:
        return user.patch(
            model= patch,
            cachePrefix= table.CACHE_PREFIX,
            id= id, 
            data= data,
            tableName= table.NAME
        )
    
    @router.delete("/{id}", response_model=DeleteResponse)
    def delete(id: int) -> DeleteResponse:
        return user.delete(
            cachePrefix= table.CACHE_PREFIX,
            id= id,
            tableName= table.NAME,
            query= table.DELETE_QUERY
        )

    return router