# Sección 1: Tres ataques de SQL injection que fallan
Por cada uno de los tres ataques debes documentar:
El input exacto que probaste (ej: ' OR '1'='1)
La pantalla del frontend donde lo metiste (descripción y/o screenshot)
Screenshot o log mostrando que el ataque falló
La línea exacta de tu código backend que defendió (archivo y número de línea)
Tipos de ataques sugeridos (no estás obligado a estos exactos):
Quote-escape clásico: ' OR '1'='1
Stacked query: '; DROP TABLE mascotas; --
Union-based: ' UNION SELECT password FROM ...
# Sección 2: Demostración de RLS en acción
Setup mínimo: dos veterinarios distintos, cada uno atendiendo mascotas diferentes (ya viene en los datos de
prueba).
Debes incluir:
Screenshot/log del veterinario 1 consultando "todas las mascotas" desde la UI y obteniendo solo las suyas
Screenshot/log del veterinario 2 haciendo la misma consulta y obteniendo otro conjunto
Una frase explicando qué política RLS produce ese comportamiento
# Sección 3: Demostración de caché Redis funcionando
Logs (con timestamps) que muestren:
Primera consulta a vacunación pendiente: cache MISS, latencia típica de BD (~100-300ms)
Segunda consulta inmediata: cache HIT, latencia típica de Redis (~5-20ms)
POST de aplicación de vacuna que invalida el caché
Tercera consulta después de la invalidación: cache MISS de nuevo
Más una explicación de qué key usaste, qué TTL elegiste, y por qué.