# Sección 1: Tres ataques de SQL injection que fallan
## ATAQUE 1
- Input usado: **rocky; delete * from mascotas**
- Captura de pantalla:
![[Pasted image 20260424223339.png]]
- Log de demostración:
![[Pasted image 20260424223039.png]]
- Línea que lo defendió:
```python
elif type == "byName":
	assert searchName is not None
	row: T = conn.execute(query, (f"%{searchName}%",)).fetchall()
```
En `baseQueries.py`, líneas *142-144*
## ATAQUE 2
- Input utilizado: 1='1
- Captura de pantalla:
![[Pasted image 20260424223619.png]]
- Log de prueba:
![[Pasted image 20260424223743.png]]
- Línea que lo defendió:
```python
elif type == "byName":
	assert searchName is not None
	row: T = conn.execute(query, (f"%{searchName}%",)).fetchall()
```
En `baseQueries.py`, líneas *142-144*
## ATAQUE 3
- Input utilizado: a
- Captura de pantalla:
![[Pasted image 20260424224040.png]]
- Log de evidencia:
![[Pasted image 20260424224128.png|652]]
- Línea que lo defendió:
```python
elif type == "byName":
	assert searchName is not None
	row: T = conn.execute(query, (f"%{searchName}%",)).fetchall()
```
En `baseQueries.py`, líneas *142-144*
# Sección 2: Demostración de RLS en acción
## Veterinario 1
- Captura de pantalla
![[Pasted image 20260424224327.png]]
- Log de evidencia
![[Pasted image 20260424224806.png]]
## Veterinario 2
- Captura de pantalla:
![[Pasted image 20260424224900.png]]
- Log de evidencia:
![[Pasted image 20260424224955.png]]

La política RLS selecciona de vet_atiende_mascotas solo a aquellas mascotas que hayan sido atendidas por ese veterinario
# Sección 3: Demostración de caché Redis funcionando
Logs (con timestamps) que muestren:
Primera consulta a vacunación pendiente: cache MISS, latencia típica de BD (~100-300ms)
Segunda consulta inmediata: cache HIT, latencia típica de Redis (~5-20ms)
POST de aplicación de vacuna que invalida el caché
Tercera consulta después de la invalidación: cache MISS de nuevo
Más una explicación de qué key usaste, qué TTL elegiste, y por qué.