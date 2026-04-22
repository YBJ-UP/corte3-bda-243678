from typing import Type

from fastapi import APIRouter

from model.response import DeleteResponse, PatchResponse, Response
from queries.userQueries import UserQueries

def create_routes[T_read, T_add, T_patch](
        user: UserQueries,
        tableAlias: str,
        tableName: str,
        cachePrefix: str,
        path: str,
        read: Type[T_read],
        add: Type[T_add],
        patch: Type[T_patch],
        readAllQuery: str,
        readOneQuery: str,
        deleteQuery: str
) -> APIRouter:
    router = APIRouter(prefix= path)

    @router.get("", response_model=Response[list[T_read]])
    def get_All() -> Response[list[T_read]]:
        return user.getAll(
            model= list[T_read],
            cachePrefix= cachePrefix,
            tableAlias= tableAlias,
            query= readAllQuery
        )
    
    @router.get("/{id}", response_model=Response[T_read])
    def get_One(id: int) -> Response[T_read]:
        return user.getOne(
            model= read,
            cachePrefix= cachePrefix,
            id= id,
            tableAlias= tableAlias,
            query= readOneQuery
        )
    
    @router.post("", response_model=Response[T_add])
    def post(data: T_add) -> PatchResponse[T_add]:
        return user.insert(
            model= add,
            cachePrefix= cachePrefix, 
            data= data,
            tableName= tableName
        )
    
    @router.patch("/{id}", response_model=Response[patch])
    def update(id: int, data: T_patch) -> PatchResponse[T_patch]:
        return user.patch(
            model= patch,
            cachePrefix= cachePrefix,
            id= id, 
            data= data,
            tableName= tableName
        )
    
    @router.delete("/{id}", response_model=DeleteResponse)
    def delete(id: int) -> DeleteResponse:
        return user.delete(
            cachePrefix= cachePrefix,
            id= id,
            tableName= tableName,
            query= deleteQuery
        )

    return router