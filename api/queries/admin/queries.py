from model.response import Response
from queries.baseQueries import BaseQueries


class AdminQueries(BaseQueries):
    ALL_OWNERS_QUERY = "SELECT * FROM duenos;"
    SELECT_OWNER_QUERY = "SELECT * FROM duenos WHERE id=%s;"
    ROLE = "Administrador"

    def getAllOwners(self, cachePrefix: str) -> Response:
        return self.get(
            type='all',
            cachePrefix=cachePrefix,
            query= self.ALL_OWNERS_QUERY,
            role= self.ROLE
        )

    def getOwner(self, cachePrefix: str, id: int) -> Response:
        return self.get(
            type="one",
            cachePrefix= cachePrefix,
            query= self.SELECT_OWNER_QUERY,
            role= self.ROLE,
            id= id
        )