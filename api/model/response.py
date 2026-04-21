from typing import TypedDict


class Response[T](TypedDict):
    cache_hit: bool
    latency_ms: float
    data: T