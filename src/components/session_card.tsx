"use client"

import Link from "next/link"
import { redirect } from "next/navigation"

interface SessionCardProps {
    name: string
    route: string
    id: string | null
    genToken: boolean
}

export default function SessionCard(data: SessionCardProps) {

    function chooseRole(input: string): string {
        switch (input.toLocaleLowerCase()) {
            case "/admin": return "a"
            case "/recep": return "r"
            case "/vet": return "v"
            default: return "inválido"
        }
    }

    async function login() {
        const role = chooseRole(data.route)
        const body = JSON.stringify({ role, id: data.id })
        console.log("iniciando sesión como: ", data.name)
        const response =  await fetch('/api/auth/login', { method: "POST", body })
        if (!response.ok) {
            console.error("No se pudo generar el token")
            redirect("/")
        }
        redirect(data.route)
    }

    return (
        <>
            {!data.genToken && (
                <Link href={data.route} className="px-10 py-5 bg-cyan-600 rounded-2xl hover:bg-cyan-500 hover:font-bold hover:scale-110">
                    <p className="text-xl">{data.name}</p>
                </Link>
        ) || (
            <div className="px-10 py-5 bg-cyan-600 rounded-2xl hover:bg-cyan-500 hover:font-bold hover:scale-110" onClick={login}>
                <p className="text-xl">{data.name}</p>
            </div>
        )}
        </>
        
        
    )
}