from queries.userQueries import UserQueries

from lib.db import pg_pool, redis_client

Admin = UserQueries(pg_pool= pg_pool, redis_client= redis_client, role= "Administrador")
Veterinario = UserQueries(pg_pool= pg_pool, redis_client= redis_client, role= "Veterinario")
Rec = UserQueries(pg_pool= pg_pool, redis_client= redis_client, role= "Recepcionista")