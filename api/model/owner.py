from pydantic import BaseModel


class Owner(BaseModel):
    id: int
    nombre: str
    telefono: str