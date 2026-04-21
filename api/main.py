from typing import Annotated

from fastapi import FastAPI, Path

from lib.db import pg_pool, redis_client, check_connections

from model.owner import Owner
from model.response import PatchResponse, Response
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
def get_owners() -> Response[list[Owner]]:
    return Admin.getAllOwners(OWNER_CACHE_PREFIX)

@app.get("/admin/owners/{id}")
def get_owner_by_id(id: Annotated[int, Path(gt=0, title="Id de usuario")]) -> Response[Owner]:
    return Admin.getOwner(OWNER_CACHE_PREFIX, id)

@app.post('/admin/owners')
def add_owner(id: Annotated[int, Path(gt=0)], data: Owner) -> PatchResponse[Owner]:
    return Admin.insertOwner(cachePrefix= OWNER_CACHE_PREFIX, data= data)