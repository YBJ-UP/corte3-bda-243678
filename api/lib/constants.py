from dataclasses import dataclass


@dataclass
class tabla:
    NAME: str
    ALIAS: str
    CACHE_PREFIX: str
    SELECT_ALL_QUERY: str
    SELECT_ONE_QUERY: str
    DELETE_QUERY: str

TABLES = {
    "OWNER": tabla(
        NAME="duenos",
        ALIAS="Dueños",
        CACHE_PREFIX="cache:owner",
        SELECT_ALL_QUERY="SELECT * FROM duenos;",
        SELECT_ONE_QUERY="SELECT * FROM duenos WHERE id=%s;",
        DELETE_QUERY="DELETE FROM duenos WHERE id=%s"
    ),
    "VET": tabla(
        NAME="veterinarios",
        ALIAS="Veterinarios",
        CACHE_PREFIX="cache:vet",
        SELECT_ALL_QUERY="SELECT * FROM veterinarios;",
        SELECT_ONE_QUERY="SELECT * FROM veterinarios WHERE id=%s",
        DELETE_QUERY="DELETE FROM veterinarios WHERE id=%s;"
    ),
    "PET": tabla(
        NAME="mascotas",
        ALIAS="Mascotas",
        CACHE_PREFIX="cache:pet",
        SELECT_ALL_QUERY="SELECT * FROM MASCOTAS;",
        SELECT_ONE_QUERY="SELECT * FROM mascotas WHERE ID=%s;",
        DELETE_QUERY="DELETE FROM mascotas WHERE id=%s;"
    ),
    "DATE": tabla(
        NAME="citas",
        ALIAS="Cita",
        CACHE_PREFIX="cache:date",
        SELECT_ALL_QUERY="SELECT * FROM citas;",
        SELECT_ONE_QUERY="SELECT * FROM citas WHERE id=%s;",
        DELETE_QUERY="DELETE FROM citas WHERE id=%s;"
    ),
    "VAXX": tabla(
        NAME="inventario_vacunas",
        ALIAS="Vacunas",
        CACHE_PREFIX="cache:vaxx",
        SELECT_ALL_QUERY="SELECT * FROM inventario_vacunas;",
        SELECT_ONE_QUERY="SELECT * FROM inventario_vacunas WHERE id=%s;",
        DELETE_QUERY="DELETE FROM inventario_vacunas WHERE id=%s;"
    )
}