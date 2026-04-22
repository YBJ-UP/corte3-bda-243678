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