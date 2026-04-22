from typing import Annotated

from pydantic import BaseModel, StringConstraints


class Owner(BaseModel):
    id: int | None = None
    nombre: Annotated[str, StringConstraints(max_length=100)]
    telefono: Annotated[str, StringConstraints(max_length=20)]
    email: Annotated[str, StringConstraints(max_length=100)]

class OwnerPost(BaseModel):
    nombre: Annotated[str, StringConstraints(max_length=100)]
    telefono: Annotated[str, StringConstraints(max_length=20)] | None = None
    email: Annotated[str, StringConstraints(max_length=100)] | None = None

class OwnerPatch(BaseModel):
    nombre: Annotated[str, StringConstraints(max_length=100)] | None = None
    telefono: Annotated[str, StringConstraints(max_length=20)] | None = None
    email: Annotated[str, StringConstraints(max_length=100)] | None = None