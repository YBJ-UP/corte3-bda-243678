import json
import time

from fastapi import FastAPI, HTTPException

from lib.db import pg_pool, redis_client, check_connections

app = FastAPI(title="TuxMascotas - Python", version="0.1.0")

OWNER_CACHE_PREFIX = "cache:owner"
CACHE_TTL = 300

ALL_OWNERS_QUERY = """
SELECT 1;
"""

@app.on_event("startup")
def startup() -> None:
    check_connections()
    print("[STARTUP] Backend listo", flush=True)

@app.get(path="/health")
def health():
    return { "success": True, "message": "Api en ejecución" }

@app.get("/admin/owners")
def get_owners():
    t0: float = time.perf_counter()
    cache_key = f"{OWNER_CACHE_PREFIX}"

    cached = redis_client.get(cache_key)
    if cached is not None:
        elapsed: float = (time.perf_counter()-t0) * 1000
        print(f"[CACHE HIT] ({elapsed:.2f})", flush=True)
        return {
            "cache_hit": True,
            "latency_ms": round(elapsed, 2),
            "data": json.loads(cached)
        }
    with pg_pool.connection() as conn:
        row = conn.execute(ALL_OWNERS_QUERY).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="No se pudieron conseguir los usuarios")
    
    print(row)