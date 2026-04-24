"use client"

import { redirect } from "next/navigation";
import { useEffect, useState } from "react";

export default function Layout({
        children,
    }: Readonly<{
        children: React.ReactNode;
}>){

    async function logout() {
        console.log("Cerrando sesión...")
        const response =  await fetch('/api/auth/logout', { method: "POST"})
        if (!response.ok) {
            console.error("No se pudo generar el token: ", await response.json())
        }
        console.log("Sesión cerrada con éxito.")
        redirect("/")
    }

    const [ name, setName ] = useState<string>("")
    const [loading, setIsLoading] = useState<boolean>(false)

    useEffect(() => {
        const fetchName = async () => {
            try {
                setIsLoading(true)
                const res = await fetch(`/api/auth/name`)
                const json = await res.json()
                setName(json.name)
            } catch {
                console.error("No se pudieron obtener los datos correctamente.")
            } finally {
                setIsLoading(false)
            }
        }
        fetchName()
    }, [])

    return (
        <>
            <div className="flex items-center justify-between bg-green-700 py-7 px-15">
                <div>
                    <h1 className="text-xl font-bold">Veterinaria TuxMascotas</h1>
                    <p>{name}</p>
                </div>
                <button className="font-medium hover:font-bold" onClick={logout}>Cerrar sesión</button>
            </div>
            <div className="m-10">
                {children}
            </div>
        </>
    )
}