from typing import Any, Type

from fastapi import APIRouter

from model.response import Response
from queries.userQueries import UserQueries

def create_routes(
        user: UserQueries,
        tableAlias: str,
        tableName: str,
        cachePrefix: str,
        path: str,
        read: Type[Any],
        add: Type[Any],
        patch: Type[Any],
        readAllQuery: str,
        readOneQuery: str,
        deleteQuery: str
) -> APIRouter:
    router = APIRouter(prefix= path)

    @router.get("/", response_model=Response[list[read]])
    def getAll() -> Response[Any]:
        return user.getAll(
            model= read,
            cachePrefix= cachePrefix,
            tableAlias= tableAlias,
            query= readAllQuery
        )
    
    return router