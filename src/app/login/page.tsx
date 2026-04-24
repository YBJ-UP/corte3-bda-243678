"use client"

import SessionCard from "@/components/session_card";
import { useEffect, useState } from "react";
import { VetProfile } from "../api/vet/login/route";

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
        <div>
            <p>inicio d sesión</p>
            {data.map((profile) => (
                <SessionCard key={profile.id} name={profile.nombre} route="" id={String(profile.id)}/>
            ))}
        </div>
    )
}