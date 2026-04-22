from typing import Annotated

from fastapi import FastAPI, Path

from lib.db import pg_pool, redis_client, check_connections
from lib.constants import TABLES

from model.owner import Owner, OwnerPatch, OwnerPost
from model.response import DeleteResponse, PatchResponse, Response
from model.vet import Vet, VetPatch, VetPost
from queries.userQueries import UserQueries

app = FastAPI(title="TuxMascotas - Python", version="0.1.0")

Admin = UserQueries(pg_pool= pg_pool, redis_client= redis_client, role= "Administrador")
Veterinario = UserQueries(pg_pool= pg_pool, redis_client= redis_client, role= "Veterinario")
Rec = UserQueries(pg_pool= pg_pool, redis_client= redis_client, role= "Recepcionista")

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

@app.get("/cache/info")
def cacheInfo():
    info = redis_client.info("stats")
    info_server = redis_client.info("server")
    info_memory = redis_client.info("memory")

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses

    return {
        "redis_version": info_server.get("redis_version"),
        "used_memory_human": info_memory.get("used_memory_human"),
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        # Evitar división por cero cuando no ha habido requests aún
        "hit_ratio": round((hits / total) * 100, 2) if total > 0 else 0.0,
        "evicted_keys": info.get("evicted_keys", 0),
        "total_keys": redis_client.dbsize(),
    }

# RUTAS DE DUEÑO

@app.get("/admin/owners")
def get_owners() -> Response[list[Owner]]:
    return Admin.getAll(
        model=list[Owner],
        cachePrefix= TABLES["OWNER"].CACHE_PREFIX,
        tableAlias= TABLES["OWNER"].ALIAS,
        query=TABLES["OWNER"].SELECT_ALL_QUERY
        )

@app.get("/admin/owners/{id}")
def get_owner_by_id(id: Annotated[int, Path(gt=0, title="Id de usuario")]) -> Response[Owner]:
    return Admin.getOne(
        model=Owner,
        cachePrefix= TABLES["OWNER"].CACHE_PREFIX,
        id=id,
        tableAlias= TABLES["OWNER"].ALIAS,
        query= TABLES["OWNER"].SELECT_ONE_QUERY)

@app.post('/admin/owners')
def add_owner(data: OwnerPost) -> PatchResponse[OwnerPost]:
    return Admin.insert(
        model= OwnerPost,
        cachePrefix= TABLES["OWNER"].CACHE_PREFIX,
        data= data,
        tableName= TABLES["OWNER"].NAME
        )

@app.patch("/admin/owners/{id}")
def patch_owner(id: int, data: OwnerPatch) -> PatchResponse[OwnerPatch]:
    return Admin.patch(
        model=OwnerPatch,
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

# RUTAS DE VETERINARIO

@app.get("/admin/vets")
def get_vets() -> Response[list[Vet]]:
    return Admin.getAll(
        model=list[Vet],
        cachePrefix= TABLES["VET"].CACHE_PREFIX,
        tableAlias= TABLES["VET"].ALIAS,
        query=TABLES["VET"].SELECT_ALL_QUERY
        )

@app.get("/admin/vets/{id}")
def get_vet_by_id(id: Annotated[int, Path(gt=0, title="Id de usuario")]) -> Response[Vet]:
    return Admin.getOne(
        model=Vet,
        cachePrefix= TABLES["VET"].CACHE_PREFIX,
        id=id,
        tableAlias= TABLES["VET"].ALIAS,
        query= TABLES["VET"].SELECT_ONE_QUERY)

@app.post('/admin/vets')
def add_vet(data: VetPost) -> PatchResponse[VetPost]:
    return Admin.insert(
        model= VetPost,
        cachePrefix= TABLES["VET"].CACHE_PREFIX,
        data= data,
        tableName= TABLES["VET"].NAME
        )

@app.patch("/admin/vets/{id}")
def patch_vet(id: int, data: VetPatch) -> PatchResponse[VetPatch]:
    return Admin.patch(
        model=VetPatch,
        cachePrefix= TABLES["VET"].CACHE_PREFIX,
        id= id,
        data= data,
        tableName= TABLES["VET"].NAME
        )

@app.delete("/admin/vets/{id}")
def delete_vet(id: int) -> DeleteResponse:
    return Admin.delete(
        cachePrefix= TABLES["VET"].CACHE_PREFIX,
        id= id,
        tableName= TABLES["VET"].NAME,
        query= TABLES["VET"].DELETE_QUERY
        )