import jwt from 'jsonwebtoken'
import { NextRequest, NextResponse } from 'next/server'

export function generateToken(name: string, role: "a" | "v" | "r" | undefined, id: number | null) {
    const SECRET: string | undefined = process.env.JWT_SECRET
    const TTL: string | undefined = process.env.JWT_TTL

    if (!SECRET) {
        return NextResponse.json({ error: "No se puede generar el token" }, { status: 500 })
    }

    if (!TTL){
        return NextResponse.json({ error: "No se puede generar el token" }, { status: 500 })
    }

    if (isNaN(Number(TTL))) {
        return NextResponse.json({ error: "Tiempo de vida inválido" }, { status: 500 })
    }

    if (!role) {
        return NextResponse.json({ error: "No hay rol" }, { status: 400 })
    }

    if (role == "v" && id === null) {
        return NextResponse.json({ error: "No se obtuvo una sesión válida" }, { status: 400 })
    }

    const token = jwt.sign({ name: name, role: role, v: id }, SECRET, { expiresIn: Number(TTL) })

    const response = NextResponse.json({ message: "Token generado con éxito" })
    response.cookies.set('token', token, {
        httpOnly: true,
        sameSite: "lax",
        maxAge: Number(TTL),
        secure: process.env.NODE_ENV === "production"
    })

    return response
}

export function destroyToken() {
    const res = NextResponse.json({ message: "Sesión cerrada" })
    res.cookies.delete("token")

    return res
}

export function getNameFromJWT(req: NextRequest) {
    const token = req.cookies.get("token")?.value

    if (!token) {
        throw new Error("No hay sesión activa")
    }

    const decoded = jwt.decode(token)
    console.log(decoded)
    
    const res = NextResponse.json({ name: decoded?.search("name") })

    return res
}