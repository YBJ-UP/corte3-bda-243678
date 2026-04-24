from fastapi import APIRouter, Depends, FastAPI

from lib.auth import get_user
from lib.db import redis_client, check_connections
from lib.constants import TABLES

from lib.roles import Admin
from model.dates import Date, DatePatch, DatePost
from model.owner import Owner, OwnerPatch, OwnerPost
from model.pet import Pet, PetPatch, PetPost
from model.response import Response
from model.vaccine import Vaccine, VaccinePatch, VaccinePost
from model.vet import Vet, VetPatch, VetPost
from queries.userQueries import UserQueries
from routes.genericRouter import create_routes

app = FastAPI(title="TuxMascotas - Python", version="0.1.0")

OwnerRoutes: APIRouter = create_routes(
    table= TABLES["OWNER"],
    path="/owner",
    read= Owner,
    add= OwnerPost,
    patch= OwnerPatch,
)
VetRoutes: APIRouter = create_routes(
    table= TABLES["VET"],
    path="/vet",
    read= Vet,
    add= VetPost,
    patch= VetPatch,
)
PetRoutes: APIRouter = create_routes(
    table= TABLES["PET"],
    path="/pet",
    read= Pet,
    add= PetPost,
    patch= PetPatch,
)
DateRoutes: APIRouter = create_routes(
    table= TABLES["DATE"],
    path="/date",
    read= Date,
    add= DatePost,
    patch= DatePatch
)
VaccineRoutes: APIRouter = create_routes(
    table= TABLES["VAXX"],
    path="/vaccine",
    read= Vaccine,
    add= VaccinePost,
    patch= VaccinePatch,
)


@app.on_event("startup") # pyright: ignore[reportDeprecated]
def startup() -> None:
    check_connections()
    print("[STARTUP] Backend listo", flush=True)

@app.get(path="/health")
def health():
    return { "success": True, "message": "Api en ejecución" }

@app.post("/cache/flush")
def flush(user: UserQueries = Depends(get_user)):
    return user.wipeAllCacheWrapper()

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


@app.get("/veterinarios")
def getVetProfiles() -> Response[list[Vet]]: # método no protegido para extraer los nombres de los vets para iniciar sesión
    return Admin.getAll(
        model= list[Vet],
        cachePrefix= TABLES["OWNER"].CACHE_PREFIX,
        tableAlias= TABLES["OWNER"].ALIAS,
        query= "SELECT id, nombre FROM veterinarios;"
    )

# Carga de endpoints
# Endpoints Admin
app.include_router(OwnerRoutes)
app.include_router(VetRoutes)
app.include_router(PetRoutes)
app.include_router(DateRoutes)
app.include_router(VaccineRoutes)
