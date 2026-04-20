from typing import Any, TypedDict


class Response(TypedDict):
    cache_hit: bool
    latency_ms: float
    data: Any