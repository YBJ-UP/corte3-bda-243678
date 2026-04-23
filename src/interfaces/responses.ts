interface response {
    message: string | null
    cache_hit: boolean
    latency_ms: number
}

export interface PatchResponse<T> extends response { // también para post
    updated_data: T
}

export interface GetResponse<T> extends response {
    data: T
}

export interface DeleteResponse {
    message: string
    cache_invalidated: boolean,
    latency__ms: number
}

export interface DeleteRequest {
    id: number
}