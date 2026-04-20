from queries.baseQueries import BaseQueries


class AdminQueries(BaseQueries):
    ALL_OWNERS_QUERY = "SELECT * FROM duenos;"

    def __FormQuery(self, Query: str) -> str:
        return f"BEGIN; SET LOCAL ROLE Administrador; {Query} COMMIT;"

    def getAllOwners(self, cachePrefix: str):
        print("hola")
        self.get(
            type='all',
            cachePrefix=cachePrefix,
            query= self.__FormQuery(self.ALL_OWNERS_QUERY)
        )