from model.response import Response
from queries.baseQueries import BaseQueries


class AdminQueries(BaseQueries):
    ALL_OWNERS_QUERY = "SELECT * FROM duenos;"
    ROLE = "Administrador"

    def getAllOwners(self, cachePrefix: str) -> Response:
        return self.get(
            type='all',
            cachePrefix=cachePrefix,
            query= self.ALL_OWNERS_QUERY,
            role= self.ROLE
        )