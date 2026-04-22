from typing import Annotated

from fastapi import Path
from pydantic import BaseModel, StringConstraints

class Vaccine(BaseModel):
    id: int
    nombre: Annotated[str, StringConstraints(max_length=80)]
    stock_actual: Annotated[int, Path(ge=0)] = 0
    stock_minimo: Annotated[int, Path(gt=0)] = 5
    costo_unitario: float

class VaccinePost(BaseModel):
    nombre: Annotated[str, StringConstraints(max_length=80)]
    stock_actual: Annotated[int, Path(ge=0)] = 0
    stock_minimo: Annotated[int, Path(gt=0)] = 5
    costo_unitario: float

class VaccinePatch(BaseModel):
    nombre: Annotated[str, StringConstraints(max_length=80)] | None = None
    stock_actual: Annotated[int, Path(ge=0)] | None = None
    stock_minimo: Annotated[int, Path(gt=0)] | None = None
    costo_unitario: float | None = None