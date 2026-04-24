from typing import Annotated

from pydantic import BaseModel, StringConstraints


class Vet(BaseModel):
    id: int
    nombre: Annotated[str, StringConstraints(max_length=100)]
    cedula: Annotated[str, StringConstraints(max_length=20)] | None = None
    dias_descanso: Annotated[str, StringConstraints(max_length=50)]
    activo: bool = True

class VetPost(BaseModel):
    nombre: Annotated[str, StringConstraints(max_length=100)]
    cedula: Annotated[str, StringConstraints(max_length=20)]
    dias_descanso: Annotated[str, StringConstraints(max_length=50)] | None = None
    activo: bool = True

class VetPatch(BaseModel):
    nombre: Annotated[str, StringConstraints(max_length=100)] | None = None
    cedula: Annotated[str, StringConstraints(max_length=20)] | None = None
    dias_descanso: Annotated[str, StringConstraints(max_length=50)] | None = None
    activo: bool = True

class VetProfile(BaseModel):
    id: int
    nombre: str