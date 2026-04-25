import { DeleteResponse, GetResponse, PatchResponse } from "@/interfaces/responses";
import { NextRequest } from "next/server";

async function buildHeaders(req: NextRequest): Promise<HeadersInit> {
    const token = req.cookies.get("token")?.value

    if (!token) {
        throw new Error("No hay sesión activa")
    }

    return {
        "Authorization": `Bearer ${token}`,
        "Content-type": "application/json"
    }
}
//T es el tipo de respuesta, R es el tipo del cuerpo, deberían ser los mismos pero están separados para que se pued cambiar el tipo de respuesta
export async function request<T, R>(req: NextRequest, method: string, path: string, body: R | null = null): Promise<T> {
    const BASE = process.env.BACKEND_URL;
    if (!BASE) {
        throw new Error('No se puede establecer conexión con el backend');
    }
    
    const headers = await buildHeaders(req)
    console.log(body)

    const response = await fetch(new URL(path, BASE), {
        method,
        headers,
        ...(body !== undefined && body !== null && { body: JSON.stringify(body) })
    })

    if (!response.ok) {
        const error = await response.json()
        throw new Error(error?.detail ?? `Error ${response.status}\n${error}`)
    }

    let res: T
    try {
        res = await response.json()
    } catch {
        throw new Error("Error al obtener la respuesta del servidor")
    }

    return res
}

export async function unprotectedRequest<T>() {
    const BASE = process.env.BACKEND_URL;
    if (!BASE) {
        throw new Error('No se puede establecer conexión con el backend');
    }

    const response = await fetch(new URL('/veterinarios', BASE))

    if (!response.ok) {
        const error = await response.json()
        throw new Error(error?.detail ?? `Error ${response.status}\n${error}`)
    }

    let res: T
    try {
        res = await response.json()
    } catch {
        throw new Error("Error al obtener la respuesta del servidor")
    }

    return res
}

export async function get<T>(path: string, req: NextRequest): Promise<GetResponse<T>> {
    return request<GetResponse<T>, null>(req, "GET", path)
}

export async function post<T, R>(path: string, req: NextRequest, body: R): Promise<PatchResponse<T>> {
    return request<PatchResponse<T>, R>(req, "POST", path, body)
}

export async function patch<T, R>(path: string, req: NextRequest, body: R): Promise<PatchResponse<T>> {
    return request<PatchResponse<T>, R>(req, "PATCH", path, body)
}

export async function remove(path: string, req: NextRequest): Promise<DeleteResponse> {
    return request<DeleteResponse, null>(req, "DELETE", path)
}

// get<Owner>('/owner', req)
// get<Owner>('/owner/1', req)
// post<Owner, OwnerPost>('/owner', req)
// patch<Owner, OwnerPatch>('/owner', req)
// remove<Owner>('/owner/1', req)