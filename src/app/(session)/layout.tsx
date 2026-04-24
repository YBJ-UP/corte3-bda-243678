"use client"

import Link from "next/link";
import { redirect } from "next/navigation";

export default function Layout({
        children,
    }: Readonly<{
        children: React.ReactNode;
}>){

    async function logout() {
        console.log("Cerrando sesión...")
        const response =  await fetch('/api/auth/logout', { method: "POST" })
        if (!response.ok) {
            console.error("No se pudo generar el token: ", await response.json())
        }
        console.log("Sesión cerrada con éxito.")
        redirect("/")
    }

    return (
        <>
            <div className="flex items-center justify-between bg-green-700 py-7 px-15">
                <h1 className="text-xl font-bold">Veterinaria TuxMascotas</h1>
                <button className="font-medium hover:font-bold" onClick={logout}>Cerrar sesión</button>
            </div>
            <div className="m-10">
                {children}
            </div>
        </>
    )
}