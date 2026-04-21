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
    )
}