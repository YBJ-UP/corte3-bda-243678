from os import getenv
from dotenv import load_dotenv
from fastapi import HTTPException, Header
import jwt

from queries.userQueries import UserQueries

from lib.roles import Admin, Veterinario, Rec

load_dotenv()
__SECRET: str = getenv("JWT_SECRET", "hola")

def get_user(auth: str = Header(...)) -> UserQueries:
    try:
        token: str = auth.removeprefix("Bearer")
        payload = jwt.decode(token, __SECRET, algorithms=["HS256"])
        role = payload.get("role")

        match role:
            case "a": return Admin
            case "v": return Veterinario
            case "r": return Rec
            case _: raise HTTPException(403, "Rol incorrecto")
    except jwt.PyJWTError:
        raise HTTPException(401, "Token inválido")