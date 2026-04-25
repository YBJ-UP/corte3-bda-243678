from typing import Literal, Type

from fastapi import APIRouter, Depends, HTTPException

from lib.auth import get_user
from lib.constants import tabla
from model.response import DeleteResponse, PatchResponse, Response
from queries.userQueries import UserQueries

def select_get_query(
        role: Literal['Administrador'] | Literal['Veterinario'] | Literal['Recepcionista'],
        table: tabla,
        getOne: bool
        ) -> str:
    print(f"Seleccionando {"1" if getOne else "muchos"} de {table.NAME} como {role}")
    if not getOne:
        if role == "Administrador" and table.SELECT_ALL_ADMIN is not None:
            return table.SELECT_ALL_ADMIN
        else:
            return table.SELECT_ALL_QUERY
    else:
        if role == "Administrador" and table.SELECT_ONE_ADMIN is not None:
            return table.SELECT_ONE_ADMIN
        else:
            return table.SELECT_ONE_QUERY

def create_routes[T_read, T_add, T_patch](
        table: tabla,
        path: str,
        read: Type[T_read],
        add: Type[T_add],
        patch: Type[T_patch]
) -> APIRouter:
    router = APIRouter(prefix= path)

    @router.get("", response_model=Response[list[read]])
    def get_All(user: UserQueries = Depends(get_user)) -> Response[list[T_read]]:
        selected_query: str = select_get_query(role= user.ROLE, table= table, getOne= False)
        return user.getAll(
            model= list[T_read],
            cachePrefix= table.CACHE_PREFIX,
            tableAlias= table.ALIAS,
            query= selected_query
        )
    
    @router.get("/{id}", response_model=Response[read])
    def get_One(id: int, user: UserQueries = Depends(get_user)) -> Response[T_read]:
        selected_query: str = select_get_query(role= user.ROLE, table= table, getOne= True)
        return user.getOne(
            model= read,
            cachePrefix= table.CACHE_PREFIX,
            id= id,
            tableAlias= table.ALIAS,
            query= selected_query
        )
    
    @router.get('/search/{name}')
    def get_by_name(name: str, user: UserQueries = Depends(get_user)) -> Response[T_read]:
        if not table.SEARCH_BY_NAME:
            raise HTTPException(404, f"La búsqueda no está disponible para {table.ALIAS}")

        res = user.getByName(
            model= read,
            cachePrefix= table.CACHE_PREFIX,
            tableAlias= table.ALIAS,
            query= table.SEARCH_BY_NAME,
            name= name
        )

        if not res["data"]:
            raise HTTPException(status_code=404, detail=f"No se encontró el {table.ALIAS} buscado")
        
        return res
    
    @router.post("", response_model=PatchResponse[add])
    def post(data: add, user: UserQueries = Depends(get_user)) -> PatchResponse[T_add]:
        return user.insert(
            model= add,
            cachePrefix= table.CACHE_PREFIX, 
            data= data,
            tableName= table.NAME
        )
    
    @router.patch("/{id}", response_model=PatchResponse[patch])
    def update(id: int, data: patch, user: UserQueries = Depends(get_user)) -> PatchResponse[T_patch]:
        return user.patch(
            model= patch,
            cachePrefix= table.CACHE_PREFIX,
            id= id, 
            data= data,
            tableName= table.NAME
        )
    
    @router.delete("/{id}", response_model=DeleteResponse)
    def delete(id: int, user: UserQueries = Depends(get_user)) -> DeleteResponse:
        return user.delete(
            cachePrefix= table.CACHE_PREFIX,
            id= id,
            tableName= table.NAME,
            query= table.DELETE_QUERY
        )

    return router