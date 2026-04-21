from model.owner import Owner
from model.response import Response
from queries.baseQueries import BaseQueries


class AdminQueries(BaseQueries):
    ALL_OWNERS_QUERY = "SELECT * FROM duenos;"
    SELECT_OWNER_QUERY = "SELECT * FROM duenos WHERE id=%s;"
    DELETE_OWNER_QUERY = "DELETE FROM duenos WHERE id:%s"
    INSERT_OWNER_QUERY = "INSERT INTO duenos (nombre, telefono, email) VALUES %s, %s, %s"
    ROLE = "Administrador"

    OWNER_TABLE_NAME = "duenos"
    OWNER_TABLE_DESCRIPTION = "dueños"

    def __convert_to_tuples[T](self, model: type[T], data: T) -> tuple[tuple[str, ...], tuple[str, ...]]:
        return (tuple(data.keys()), tuple(data.values()))
    
    def __prepare_clauses(self, keys: tuple[str,...]) -> list[str]:
        clauses: list[str] = []
        for key in keys:
            clauses.append(f"{key}= %s")
        return clauses

    def __prepare_query[T](self, model: type[T], isPatch: bool, data: T, id: int, tableName: str) -> tuple[str, tuple[str,...]]:
        keys, values = self.__convert_to_tuples(model= model, data= data)

        clauses: list[str] = self.__prepare_clauses(keys)
        
        preparedQuery: str = ''
        if isPatch:
            preparedQuery: str = f"UPDATE {tableName} SET {", ".join(clauses)} WHERE ID = %s RETURNING *;"
        else:
            preparedQuery: str = ""
        
        valuesList: list[str] = list(values)
        valuesList.append(str(id))

        return preparedQuery, tuple(valuesList)
    
    def __add_or_patch(self, isPatch: bool, cachePrefix: str, query: str, values: tuple[str,...], id: int):
        if isPatch:
                return self.patch_insert(
                model= Owner,
                isPatch= True,
                cachePrefix= cachePrefix,
                tableName= self.OWNER_TABLE_NAME,
                query= query,
                params= values,
                role= self.ROLE,
                id= id
            )
        else:
            return self.patch_insert(
                model= Owner,
                isPatch= False,
                cachePrefix= cachePrefix,
                tableName= self.OWNER_TABLE_NAME,
                query= query,
                params= values,
                role= self.ROLE,
                id= id
            )

    def wipeAllCacheWrapper(self): # a canijo le di enter y me lo autocompletó
        return self.wipeAllCache(self.ROLE)

    def getAllOwners(self, cachePrefix: str) -> Response[list[Owner]]:
        return self.get(
            type='all',
            model= list[Owner],
            cachePrefix=cachePrefix,
            tableName= self.OWNER_TABLE_DESCRIPTION,
            query= self.ALL_OWNERS_QUERY,
            role= self.ROLE
        )

    def getOwner(self, cachePrefix: str, id: int) -> Response[Owner]:
        return self.get(
            type="one",
            model= Owner,
            cachePrefix= cachePrefix,
            tableName= self.OWNER_TABLE_NAME,
            query= self.SELECT_OWNER_QUERY,
            role= self.ROLE,
            id= id
        )
    
    def patchOwner(self, cachePrefix: str, id: int, data: Owner):
        query, values = self.__prepare_query(model= Owner, isPatch= True, data= data, id= id, tableName= self.OWNER_TABLE_NAME)
        return self.__add_or_patch(
            isPatch= True,
            cachePrefix= cachePrefix,
            query= query,
            values= values,
            id= id
        )
    
    def deleteOwner(self, cachePrefix: str, id: int):
        return self.delete(
            model= Owner,
            cachePrefix= cachePrefix,
            tableName= self.OWNER_TABLE_NAME,
            query= self.DELETE_OWNER_QUERY,
            role= self.ROLE,
            id= id
        )