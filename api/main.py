from typing import Annotated

from fastapi import FastAPI, Path

from lib.db import pg_pool, redis_client, check_connections

from model.characterValidator import Validator
from model.owner import Owner
from model.response import Response
from queries.admin.queries import AdminQueries

app = FastAPI(title="TuxMascotas - Python", version="0.1.0")
validator = Validator()
Admin = AdminQueries(pg_pool= pg_pool, redis_client= redis_client, validator= validator)

OWNER_CACHE_PREFIX = "cache:owner:"

@app.on_event("startup") # pyright: ignore[reportDeprecated]
def startup() -> None:
    check_connections()
    print("[STARTUP] Backend listo", flush=True)

@app.get(path="/health")
def health():
    return { "success": True, "message": "Api en ejecución" }

@app.get("/admin/owners")
def get_owners() -> Response[list[Owner]]:
    return Admin.getAllOwners(OWNER_CACHE_PREFIX)

@app.get("/admin/owners/{id}")
def get_owner_by_id(id: Annotated[int, Path(gt=0, title="Id de usuario")]) -> Response[Owner]:
    return Admin.getOwner(OWNER_CACHE_PREFIX, id)