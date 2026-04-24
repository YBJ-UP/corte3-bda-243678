from os import getenv
from dotenv import load_dotenv

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import jwt

from queries.userQueries import UserQueries
from lib.roles import Admin, Veterinario, Rec

load_dotenv()
__SECRET: str = getenv("JWT_SECRET", "ejemplo-no-se")

bearer = HTTPBearer()

def get_user(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> UserQueries:
    try:
        payload = jwt.decode(credentials.credentials, __SECRET, algorithms=["HS256"])
        role: str | None = payload.get("role")
        print(payload)

        match role:
            case "a": return Admin
            case "v":
                vet_id: str | None = payload.get("v")
                if not isinstance(vet_id, int):
                    raise HTTPException(403, "Token inválido")
                return Veterinario.appendId(vet_id)
            case "r": return Rec
            case _: raise HTTPException(403, "Rol incorrecto")
    except jwt.PyJWTError:
        raise HTTPException(401, "Token inválido")