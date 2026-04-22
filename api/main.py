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
    table= TABLES["OWNER"],
    path="/admin/owners",
    read= Owner,
    add= OwnerPost,
    patch= OwnerPatch,
)
AdminVetRoutes: APIRouter = create_routes(
    user= Admin,
    table= TABLES["VET"],
    path="/admin/vet",
    read= Vet,
    add= VetPost,
    patch= VetPatch,
)
AdminPetRoutes: APIRouter = create_routes(
    user= Admin,
    table= TABLES["PET"],
    path="/admin/pet",
    read= Pet,
    add= PetPost,
    patch= PetPatch,
)
AdminDateRoutes: APIRouter = create_routes(
    user= Admin,
    table= TABLES["DATE"],
    path="/admin/date",
    read= Date,
    add= DatePost,
    patch= DatePatch
)
AdminVaccineRoutes: APIRouter = create_routes(
    user= Admin,
    table= TABLES["VAXX"],
    path="/admin/vaccines",
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