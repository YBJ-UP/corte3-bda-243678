from fastapi import HTTPException

from model.response import Response
from queries.baseQueries import BaseQueries


class AdminQueries(BaseQueries):
    ALL_OWNERS_QUERY = "SELECT * FROM duenos;"
    SELECT_OWNERS_QUERY = "SELECT * FROM duenos WHERE id=;"
    ROLE = "Administrador"

    def getAllOwners(self, cachePrefix: str) -> Response:
        return self.get(
            type='all',
            cachePrefix=cachePrefix,
            query= self.ALL_OWNERS_QUERY,
            role= self.ROLE
        )

    def getOwner(self, cachePrefix: str, id: int) -> Response:
        isValid, invalidChar = self.validator.validateField(field=str(id))
        if not isValid:
            raise HTTPException(400, f"Caracter inválido: {invalidChar}")
        
        return self.get(
            type="one",
            cachePrefix= cachePrefix,
            query= f"SELECT * FROM duenos WHERE id={id};",
            role= self.ROLE,
            id= id
        )