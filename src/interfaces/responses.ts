interface response {
    message: string | null
    cache_hit: boolean
    latency_ms: number
}

export interface PatchResponse<T> extends response {
    updated_data: T
}

export interface GetResponse<T> extends response {
    data: T
}