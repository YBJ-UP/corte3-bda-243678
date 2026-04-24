"use client"

import SessionCard from "@/components/session_card";
import { useEffect, useState } from "react";
import { VetProfile } from "../api/vet/login/route";
import Link from "next/link";

export default function Login() {
    const [data, setData] = useState<VetProfile[]>([])
    const [loading, setIsLoading] = useState<boolean>(false)
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsLoading(true)
                const res = await fetch('/api/vet/login')
                const json = await res.json()
                setData(json.data)
            } catch {
                console.error("XD")
            } finally {
                setIsLoading(false)
            }
        }
        fetchData()
    }, [])

    return (
        <section className="flex justify-center items-center gap-25 my-auto">
            <div>
                <h1 className="text-2xl font-extrabold">¡Bienvenido a TuxMascotas!</h1>
                <h2 className="text-xl font-semibold">Inicie sesión como:</h2>
                <Link href={'/'} className="text-sm text-blue-600 hover:text-blue-500 hover:font-semibold">Regresar al menú principal</Link>
            </div>
                <section className="flex flex-col gap-5 w-100">
                    {loading && (
                        <p className="text-xl font-semibold">Cargando...</p>
                    )}
                    {data.map((profile) => (
                    <SessionCard key={profile.id} name={profile.nombre} route="/vet" id={String(profile.id)} genToken={true} />
                ))}
                </section>
            </section>
    )
}