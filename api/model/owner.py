from typing import Annotated

from pydantic import BaseModel, StringConstraints


class Owner(BaseModel):
    id: int
    nombre: Annotated[str, StringConstraints(max_length=100)]
    telefono: Annotated[str, StringConstraints(max_length=20)] | None = None
    email: Annotated[str, StringConstraints(max_length=100)] | None = None