from datetime import date
from typing import Annotated

from pydantic import BaseModel, StringConstraints

class Pet(BaseModel):
    id: int
    nombre: Annotated[str, StringConstraints(max_length=50)]
    especie: Annotated[str, StringConstraints(max_length=30)]
    fecha_nacimiento: date
    dueno_id: int

class PetPost(BaseModel):
    nombre: Annotated[str, StringConstraints(max_length=50)]
    especie: Annotated[str, StringConstraints(max_length=30)]
    fecha_nacimiento: date | None = None
    dueno_id: int

class PetPatch(BaseModel):
    nombre: Annotated[str, StringConstraints(max_length=50)] | None = None
    especie: Annotated[str, StringConstraints(max_length=30)] | None = None
    fecha_nacimiento: date | None = None
    dueno_id: int | None = None