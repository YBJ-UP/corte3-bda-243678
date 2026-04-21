from typing import Annotated

from fastapi import FastAPI, Path

from lib.db import pg_pool, redis_client, check_connections
from lib.constants import TABLES

from model.owner import OwnerBaseModel
from model.response import DeleteResponse, PatchResponse, Response
from queries.admin.queries import AdminQueries

app = FastAPI(title="TuxMascotas - Python", version="0.1.0")

Admin = AdminQueries(pg_pool= pg_pool, redis_client= redis_client)

OWNER_CACHE_PREFIX = "cache:owner"

@app.on_event("startup") # pyright: ignore[reportDeprecated]
def startup() -> None:
    check_connections()
    print("[STARTUP] Backend listo", flush=True)

@app.get(path="/health")
def health():
    return { "success": True, "message": "Api en ejecución" }

@app.post("/cache/flush")
def flush():
    return Admin.wipeAllCacheWrapper()

@app.get("/admin/owners")
def get_owners() -> Response[list[OwnerBaseModel]]:
    return Admin.getAll(
        model=list[OwnerBaseModel],
        cachePrefix= TABLES["OWNER"].CACHE_PREFIX,
        tableAlias= TABLES["OWNER"].ALIAS,
        query=TABLES["OWNER"].SELECT_ALL_QUERY
        )

@app.get("/admin/owners/{id}")
def get_owner_by_id(id: Annotated[int, Path(gt=0, title="Id de usuario")]) -> Response[OwnerBaseModel]:
    return Admin.getOne(
        model=OwnerBaseModel,
        cachePrefix= TABLES["OWNER"].CACHE_PREFIX,
        id=id,
        tableAlias= TABLES["OWNER"].ALIAS,
        query= TABLES["OWNER"].SELECT_ONE_QUERY)

@app.post('/admin/owners')
def add_owner(data: OwnerBaseModel) -> PatchResponse[OwnerBaseModel]:
    return Admin.insert(
        cachePrefix= TABLES["OWNER"].CACHE_PREFIX,
        data= data,
        tableName= TABLES["OWNER"].NAME
        )

@app.patch("/admin/owners/{id}")
def patch_owner(id: int, data: OwnerBaseModel) -> PatchResponse[OwnerBaseModel]:
    return Admin.patch(
        model=OwnerBaseModel,
        cachePrefix= TABLES["OWNER"].CACHE_PREFIX,
        id= id,
        data= data,
        tableName= TABLES["OWNER"].NAME
        )

@app.delete("/admin/owners/{id}")
def delete_owner(id: int) -> DeleteResponse:
    return Admin.delete(
        cachePrefix= TABLES["OWNER"].CACHE_PREFIX,
        id= id,
        tableName= TABLES["OWNER"].NAME,
        query= TABLES["OWNER"].DELETE_QUERY
        )