from fastapi import APIRouter, FastAPI

from lib.db import pg_pool, redis_client, check_connections
from lib.constants import TABLES

from model.dates import Date, DatePatch, DatePost
from model.owner import Owner, OwnerPatch, OwnerPost
from model.pet import Pet, PetPatch, PetPost
from model.vaccine import Vaccine, VaccinePatch, VaccinePost
from model.vet import Vet, VetPatch, VetPost
from queries.userQueries import UserQueries
from routes.genericRouter import create_routes

app = FastAPI(title="TuxMascotas - Python", version="0.1.0")

Admin = UserQueries(pg_pool= pg_pool, redis_client= redis_client, role= "Administrador")
Veterinario = UserQueries(pg_pool= pg_pool, redis_client= redis_client, role= "Veterinario")
Rec = UserQueries(pg_pool= pg_pool, redis_client= redis_client, role= "Recepcionista")

AdminOwnerRoutes: APIRouter = create_routes(
    user= Admin,
    tableAlias= TABLES["OWNER"].ALIAS,
    tableName= TABLES["OWNER"].NAME,
    cachePrefix= TABLES["OWNER"].CACHE_PREFIX,
    path="/admin/owners",
    read= Owner,
    add= OwnerPost,
    patch= OwnerPatch,
    readAllQuery= TABLES["OWNER"].SELECT_ALL_QUERY,
    readOneQuery= TABLES["OWNER"].SELECT_ONE_QUERY,
    deleteQuery= TABLES["OWNER"].DELETE_QUERY
)

AdminVetRoutes: APIRouter = create_routes(
    user= Admin,
    tableAlias= TABLES["VET"].ALIAS,
    tableName= TABLES["VET"].NAME,
    cachePrefix= TABLES["VET"].CACHE_PREFIX,
    path="/admin/vet",
    read= Vet,
    add= VetPost,
    patch= VetPatch,
    readAllQuery= TABLES["VET"].SELECT_ALL_QUERY,
    readOneQuery= TABLES["VET"].SELECT_ONE_QUERY,
    deleteQuery= TABLES["VET"].DELETE_QUERY
)

AdminPetRoutes: APIRouter = create_routes(
    user= Admin,
    tableAlias= TABLES["PET"].ALIAS,
    tableName= TABLES["PET"].NAME,
    cachePrefix= TABLES["PET"].CACHE_PREFIX,
    path="/admin/pet",
    read= Pet,
    add= PetPost,
    patch= PetPatch,
    readAllQuery= TABLES["PET"].SELECT_ALL_QUERY,
    readOneQuery= TABLES["PET"].SELECT_ONE_QUERY,
    deleteQuery= TABLES["PET"].DELETE_QUERY
)

AdminDateRoutes: APIRouter = create_routes(
    user= Admin,
    tableAlias= TABLES["DATE"].ALIAS,
    tableName= TABLES["DATE"].NAME,
    cachePrefix= TABLES["DATE"].CACHE_PREFIX,
    path="/admin/date",
    read= Date,
    add= DatePost,
    patch= DatePatch,
    readAllQuery= TABLES["DATE"].SELECT_ALL_QUERY,
    readOneQuery= TABLES["DATE"].SELECT_ONE_QUERY,
    deleteQuery= TABLES["DATE"].DELETE_QUERY
)

AdminVaccineRoutes: APIRouter = create_routes(
    user= Admin,
    tableAlias= TABLES["VAXX"].ALIAS,
    tableName= TABLES["VAXX"].NAME,
    cachePrefix= TABLES["VAXX"].CACHE_PREFIX,
    path="/admin/vaccines",
    read= Vaccine,
    add= VaccinePost,
    patch= VaccinePatch,
    readAllQuery= TABLES["VAXX"].SELECT_ALL_QUERY,
    readOneQuery= TABLES["VAXX"].SELECT_ONE_QUERY,
    deleteQuery= TABLES["VAXX"].DELETE_QUERY
)

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

# Carga de endpoints
# Endpoints Admin
app.include_router(AdminOwnerRoutes)
app.include_router(AdminVetRoutes)
app.include_router(AdminPetRoutes)
app.include_router(AdminDateRoutes)
app.include_router(AdminVaccineRoutes)