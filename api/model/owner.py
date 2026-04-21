from typing import Annotated

from pydantic import BaseModel, StringConstraints


class OwnerBaseModel(BaseModel):
    id: int | None = None
    nombre: Annotated[str, StringConstraints(max_length=100)] | None = None
    telefono: Annotated[str, StringConstraints(max_length=20)] | None = None
    email: Annotated[str, StringConstraints(max_length=100)] | None = None