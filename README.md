Esta es una aplicación web full stack para una plataforma de veterinaria.
## ¿Qué política RLS aplicaste a la tabla mascotas?
Pega la cláusula exacta y explica con tus palabras qué hace.
## Cualquiera que sea la estrategia que elegiste para identificar al veterinario actual en RLS, tiene un vector de ataque posible. ¿Cuál es? ¿Tu sistema lo previene? ¿Cómo?
## Si usas SECURITY DEFINER en algún procedure, ¿qué medida específica tomaste para prevenir la escalada de
privilegios que ese modo habilita? Si no lo usas, justifica por qué no era necesario.
## ¿Qué TTL le pusiste al caché Redis y por qué ese valor específico? ¿Qué pasaría si fuera demasiado bajo? ¿Demasiado alto?
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
Lista tres operaciones que se romperían.
1. 