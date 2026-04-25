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
## Primera consulta
```json
{ "cache_hit": false, "latency_ms": 11.31, "data": [ { "id": 1, "nombre": "Antirrábica canina", "stock_actual": 25, "stock_minimo": 10, "costo_unitario": 350 }, { "id": 2, "nombre": "Quíntuple felina", "stock_actual": 18, "stock_minimo": 8, "costo_unitario": 480 }, { "id": 3, "nombre": "Parvovirus canino", "stock_actual": 12, "stock_minimo": 5, "costo_unitario": 290 }, { "id": 4, "nombre": "Triple felina", "stock_actual": 7, "stock_minimo": 8, "costo_unitario": 410 }, { "id": 5, "nombre": "Bordetella canina", "stock_actual": 20, "stock_minimo": 10, "costo_unitario": 270 }, { "id": 6, "nombre": "Leucemia felina", "stock_actual": 4, "stock_minimo": 5, "costo_unitario": 520 } ] }
```
## Segunda consulta
```json
{ "cache_hit": true, "latency_ms": 0.65, "data": [ { "id": 1, "nombre": "Antirrábica canina", "stock_actual": 25, "stock_minimo": 10, "costo_unitario": 350 }, { "id": 2, "nombre": "Quíntuple felina", "stock_actual": 18, "stock_minimo": 8, "costo_unitario": 480 }, { "id": 3, "nombre": "Parvovirus canino", "stock_actual": 12, "stock_minimo": 5, "costo_unitario": 290 }, { "id": 4, "nombre": "Triple felina", "stock_actual": 7, "stock_minimo": 8, "costo_unitario": 410 }, { "id": 5, "nombre": "Bordetella canina", "stock_actual": 20, "stock_minimo": 10, "costo_unitario": 270 }, { "id": 6, "nombre": "Leucemia felina", "stock_actual": 4, "stock_minimo": 5, "costo_unitario": 520 } ] }
```
## POST de vacuna
```json
{ "message": "Dato actualizado con éxito.", "cache_invalidated": true, "latency_ms": 13.54, "updated_data": { "nombre": "vanuca", "stock_actual": 110, "stock_minimo": 50, "costo_unitario": 111110 } }
```
## Tercera consulta
```json
{ "cache_hit": false, "latency_ms": 28.52, "data": [ { "id": 1, "nombre": "Antirrábica canina", "stock_actual": 25, "stock_minimo": 10, "costo_unitario": 350 }, { "id": 2, "nombre": "Quíntuple felina", "stock_actual": 18, "stock_minimo": 8, "costo_unitario": 480 }, { "id": 3, "nombre": "Parvovirus canino", "stock_actual": 12, "stock_minimo": 5, "costo_unitario": 290 }, { "id": 4, "nombre": "Triple felina", "stock_actual": 7, "stock_minimo": 8, "costo_unitario": 410 }, { "id": 5, "nombre": "Bordetella canina", "stock_actual": 20, "stock_minimo": 10, "costo_unitario": 270 }, { "id": 6, "nombre": "Leucemia felina", "stock_actual": 4, "stock_minimo": 5, "costo_unitario": 520 }, { "id": 7, "nombre": "vanuca", "stock_actual": 110, "stock_minimo": 50, "costo_unitario": 111110 } ] }
```
## Explicación de llaves
Se utilizó el prefijo `{rol}:cache:{tabla}` para la cuenta de administrador y recepcionista, mientras que se usó `{rol}:cache:{tabla}:{id}` para los veterinarios.
Esto se hizo para poder distinguir bien qué usuarios están accediendo al caché, mientras que se le añadió el id a la caché por que si no, todos los veterinarios compartirían el mismo caché, llevando a que puedan ver datos que no deberían poder ver.
## Tiempo de vida utilizado
Se decidió utilizar un tiempo de vida de 1 hora debido al contexto de la aplicación, típicamente las veterinarias no son tan activas y no necesitan que se cambie el caché tan seguido pero a su vez no de decidió un tiempo de vida demasiado largo,