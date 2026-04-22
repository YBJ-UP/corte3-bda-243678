from datetime import datetime
from typing import Literal

from pydantic import BaseModel

class Date(BaseModel):
    id: int
    mascota_id: int
    veterinario_id: int
    fecha_hora: datetime
    motivo: str
    costo: float
    estado: Literal["AGENDADA", "COMPLETADA", "CANCELADA"] = "AGENDADA"

class DatePost(BaseModel):
    mascota_id: int
    veterinario_id: int
    fecha_hora: datetime
    motivo: str | None = None
    costo: float | None = None
    estado: Literal["AGENDADA", "COMPLETADA", "CANCELADA"] = "AGENDADA"

class DatePatch(BaseModel):
    mascota_id: int | None = None
    veterinario_id: int | None = None
    fecha_hora: datetime | None = None
    motivo: str | None = None
    costo: float | None = None
    estado: Literal["AGENDADA", "COMPLETADA", "CANCELADA"] | None = None