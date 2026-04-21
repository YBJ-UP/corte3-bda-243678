from typing import TypedDict


class Response[T](TypedDict):
    cache_hit: bool
    latency_ms: float
    data: T

class PatchResponse[T](TypedDict):
    message: str
    cache_invalidated: bool
    latency_ms: float
    updated_data: T

class DeleteResponse(TypedDict):
    message: str
    cache_invalidated: bool
    latency_ms: float

# hola: Response[DeleteResponse] = { "cache_hit":True, "latency_ms":67.67, "data": { "cache_invalidated":True, "latency_ms":67.00, "message":"lol" } }
# crayola = tuple(hola.values())
# print(crayola) #prueba de concepto para sacarle las llaves de manera automatica, la vd no se para qué sería, supongo que para que los update sean dinámicos, si hay null lo pondria en la base
