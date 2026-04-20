from os import getenv
from sys import exit
from dotenv import load_dotenv

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from redis import Redis, ConnectionPool as RedisPool

load_dotenv()
_db_url: str = getenv("POSTGRES_URL", "postgres://app:12345678@postgres:5432/postgres")

pg_pool = ConnectionPool(
    conninfo= _db_url,
    min_size=2,
    max_size=10,
    kwargs={"row_factory": dict_row}
)

_redis_url: str = getenv("REDIS_URL", "redis://redis:6739/0")

# Formato: redis://host:port/db
_redis_parts = _redis_url.replace("redis://", "").split("/")
_redis_host_port = _redis_parts[0].split(":")
_redis_host = _redis_host_port[0]
_redis_port = int(_redis_host_port[1]) if len(_redis_host_port) > 1 else 6379
_redis_db = int(_redis_parts[1]) if len(_redis_parts) > 1 else 0

_redis_pool = RedisPool(
    host=_redis_host,
    port=_redis_port,
    db=_redis_db,
    # decode_responses=True devuelve str en vez de bytes,
    # así json.loads() funciona directo sin necesidad de .decode()
    decode_responses=True,
    max_connections=20,
)

redis_client = Redis(connection_pool=_redis_pool)

def check_connections() -> None:
    """Verifica que ambas conexiones estén activas al arrancar.
    Si alguna falla, el proceso termina con exit code 1."""
    try:
        redis_client.ping()
        print("[startup] Redis: OK", flush=True)
    except Exception as e:
        print(f"[startup] Redis: FALLO - {e}", flush=True)
        exit(1)

    try:
        with pg_pool.connection() as conn:
            conn.execute("SELECT 1")
        print("[startup] PostgreSQL: OK", flush=True)
    except Exception as e:
        print(f"[startup] PostgreSQL: FALLO - {e}", flush=True)
        exit(1)