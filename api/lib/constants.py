from dataclasses import dataclass
from tkinter import SEL


@dataclass
class tabla:
    NAME: str
    ALIAS: str
    CACHE_PREFIX: str
    SELECT_ALL_QUERY: str
    SELECT_ALL_ADMIN: str | None
    SELECT_ONE_QUERY: str
    SELECT_ONE_ADMIN: str | None
    DELETE_QUERY: str

TABLES = {
    "OWNER": tabla(
        NAME="duenos",
        ALIAS="Dueños",
        CACHE_PREFIX="cache:owner",
        SELECT_ALL_QUERY="SELECT * FROM duenos;",
        SELECT_ALL_ADMIN= None,
        SELECT_ONE_QUERY="SELECT * FROM duenos WHERE id=%s;",
        SELECT_ONE_ADMIN= None,
        DELETE_QUERY="DELETE FROM duenos WHERE id=%s RETURNING id;"
    ),
    "VET": tabla(
        NAME="veterinarios",
        ALIAS="Veterinarios",
        CACHE_PREFIX="cache:vet",
        SELECT_ALL_QUERY="SELECT id, nombre, dias_descanso FROM veterinarios WHERE activo = true;",
        SELECT_ALL_ADMIN= "SELECT * FROM veterinarios;",
        SELECT_ONE_QUERY="SELECT id, nombre, dias_descanso FROM veterinarios WHERE id=%s AND activo = true",
        SELECT_ONE_ADMIN= "SELECT * FROM veterinarios WHERE id=%s",
        DELETE_QUERY="DELETE FROM veterinarios WHERE id=%s RETURNING id;"
    ),
    "PET": tabla(
        NAME="mascotas",
        ALIAS="Mascotas",
        CACHE_PREFIX="cache:pet",
        SELECT_ALL_QUERY="SELECT * FROM mascotas;",
        SELECT_ALL_ADMIN= None,
        SELECT_ONE_QUERY="SELECT * FROM mascotas WHERE id=%s;",
        SELECT_ONE_ADMIN= None,
        DELETE_QUERY="DELETE FROM mascotas WHERE id=%s RETURNING id;"
    ),
    "DATE": tabla(
        NAME="citas",
        ALIAS="Cita",
        CACHE_PREFIX="cache:date",
        SELECT_ALL_QUERY="SELECT * FROM citas;",
        SELECT_ALL_ADMIN= None,
        SELECT_ONE_QUERY="SELECT * FROM citas WHERE id=%s;",
        SELECT_ONE_ADMIN= None,
        DELETE_QUERY="DELETE FROM citas WHERE id=%s RETURNING id;"
    ),
    "VAXX": tabla(
        NAME="inventario_vacunas",
        ALIAS="Vacunas",
        CACHE_PREFIX="cache:vaxx",
        SELECT_ALL_QUERY="SELECT * FROM inventario_vacunas;",
        SELECT_ALL_ADMIN= None,
        SELECT_ONE_QUERY="SELECT * FROM inventario_vacunas WHERE id=%s;",
        SELECT_ONE_ADMIN= None,
        DELETE_QUERY="DELETE FROM inventario_vacunas WHERE id=%s RETURNING id;"
    ),
    "VAC_AP": tabla(
        NAME= "vacunas_aplicadas",
        ALIAS="Vacunas aplicadas",
        CACHE_PREFIX="cache:aplicadas",
        SELECT_ALL_QUERY="SELECT * FROM vacunas_aplicadas;",
        SELECT_ALL_ADMIN= None,
        SELECT_ONE_QUERY= "SELECT * FROM vacunas_aplicadas WHERE id=%s;",
        SELECT_ONE_ADMIN= None,
        DELETE_QUERY= "DELETE FROM vacunas_aplicadas WHERE id=%s RETURNING id;"
    ),
    "VAM": tabla(
        NAME= "vet_atiende_mascota",
        ALIAS="Mascotas atendidas por veterinario",
        CACHE_PREFIX="cache:vap",
        SELECT_ALL_QUERY="SELECT * FROM vet_atiende_mascotas;",
        SELECT_ALL_ADMIN= None,
        SELECT_ONE_QUERY= "SELECT * FROM vet_atiende_mascotas WHERE id=%s;",
        SELECT_ONE_ADMIN= None,
        DELETE_QUERY= "DELETE FROM vet_atiende_mascotas WHERE id=%s RETURNING id;"
    ),
    "HIST": tabla(
        NAME= "historial_movimientos",
        ALIAS="Historial de movimientos",
        CACHE_PREFIX="cache:historial",
        SELECT_ALL_QUERY="SELECT * FROM historial_movimientos;",
        SELECT_ALL_ADMIN= None,
        SELECT_ONE_QUERY= "SELECT * FROM historial_movimientos WHERE id=%s;",
        SELECT_ONE_ADMIN= None,
        DELETE_QUERY= "DELETE FROM historial_movimientos WHERE id=%s RETURNING id;"
    ),
    "ALERTS": tabla(
        NAME= "alertas",
        ALIAS="Alertas",
        CACHE_PREFIX="cache:alerts",
        SELECT_ALL_QUERY="SELECT * FROM alertas;",
        SELECT_ALL_ADMIN= None,
        SELECT_ONE_QUERY= "SELECT * FROM alertas WHERE id=%s;",
        SELECT_ONE_ADMIN= None,
        DELETE_QUERY= "DELETE FROM alertas WHERE id=%s RETURNING id;"
    ),
}