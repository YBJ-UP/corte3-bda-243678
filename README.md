Esta es una aplicación web full stack para una plataforma de veterinaria.
## ¿Qué política RLS aplicaste a la tabla mascotas?
```sql
CREATE POLICY mascotas_vet ON mascotas
    FOR ALL TO veterinario 
    USING (
        id IN (
            SELECT mascota_id 
            FROM vet_atiende_mascota 
            WHERE vet_id = current_setting('app.current_id')::int
        )
    );
```
Esta política hace un select en vet_atiende_mascotas, filtrándolo por el id del usuario actual y solo devuelve los ids de las mascotas que se hayan seleccionado.
## Cualquiera que sea la estrategia que elegiste para identificar al veterinario actual en RLS, tiene un vector de ataque posible. ¿Cuál es? ¿Tu sistema lo previene? ¿Cómo?
## ¿Qué TTL le pusiste al caché Redis y por qué ese valor específico? ¿Qué pasaría si fuera demasiado bajo? ¿Demasiado alto?
El tiempo de vida del caché de Redis es de una hora, se decidió este valor ya que es para un negocio que no ve actividad continua, pero no se escogió una duración más alta para evitar consumo de memoria innecesario. Si este fuese más bajo, existiría la posibilidad de que varios usuarios intenten acceder al caché poco después de que este expirara, haciendo conexiones excesivas a la base de datos.
## Manejo de inputs en el backend
Ya que el backend utiliza psycopg y pydantic, no se hacen muchas verificaciones explícitas debido a que estas librerías ya las manejan, sin embargo, se hace lo siguiente:
1. Queries parametrizadas:
`api/lib/constants.py`, líneas *17-27*
```python
    "OWNER": tabla(
        NAME="duenos",
        ALIAS="Dueños",
        CACHE_PREFIX="cache:owner",
        SELECT_ALL_QUERY="SELECT * FROM duenos;",
        SELECT_ALL_ADMIN= None,
        SELECT_ONE_QUERY="SELECT * FROM duenos WHERE id=%s;",
        SELECT_ONE_ADMIN= None,
        SEARCH_BY_NAME= "SELECT * FROM duenos WHERE nombre ILIKE %s;",
        DELETE_QUERY="DELETE FROM duenos WHERE id=%s RETURNING id;"
	)
```
Esto se hace con todas las queries

`/api/queries/baseQueries.py`, líneas *51-69*
```python
    def __prepare_clauses(self, keys: tuple[str,...]) -> list[str]:
        clauses: list[str] = []
        for key in keys:
            clauses.append(f"{key}= %s")
        return clauses

    def __prepare_query[T](self, model: type[T], isPatch: bool, data: T, tableName: str, id: int | None = None) -> tuple[str, tuple[str,...]]:
        keys, values = self.__convert_to_tuples(model= model, data= data)
        clauses: list[str] = self.__prepare_clauses(keys)
        valuesList: list[str] = list(values)
        preparedQuery: str = ''
        if isPatch:
            assert id is not None
            preparedQuery: str = f"UPDATE {tableName} SET {", ".join(clauses)} WHERE ID = %s RETURNING *;"
            valuesList.append(str(id))
        else:
            preparedQuery: str = f"INSERT INTO {tableName} ({", ".join(keys)}) VALUES ({", ".join(["%s"] * len(keys))}) RETURNING *;"
```
En este fragmento se preparan las consultas para PATCH y POST de manera que sean consultas parametrizadas, asegurando que no se puedan hacer inyecciones SQL.
## Si revocas todos los permisos del rol de veterinario excepto SELECT en mascotas, ¿qué deja de funcionar en tu sistema?
1. No se podrían actualizar los datos de las mascotas
2. No aplicarían todas las políticas de RLS
3. Sinceramente no veo una tercera cosa profe :c