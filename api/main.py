from fastapi import FastAPI

from lib.db import pg_pool, redis_client, check_connections

from model.response import Response
from queries.admin.queries import AdminQueries

app = FastAPI(title="TuxMascotas - Python", version="0.1.0")
Admin = AdminQueries(pg_pool, redis_client)

OWNER_CACHE_PREFIX = "cache:owner"
CACHE_TTL = 300

@app.on_event("startup") # pyright: ignore[reportDeprecated]
def startup() -> None:
    check_connections()
    print("[STARTUP] Backend listo", flush=True)

@app.get(path="/health")
def health():
    return { "success": True, "message": "Api en ejecución" }

@app.get("/admin/owners")
def get_owners() -> Response:
    return Admin.getAllOwners(OWNER_CACHE_PREFIX)