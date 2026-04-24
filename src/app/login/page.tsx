"use client"

import SessionCard from "@/components/session_card";
import { useEffect, useState } from "react";
import { VetProfile } from "../api/vet/login/route";

export default function Login() {
    const [data, setData] = useState<VetProfile[]>([])
    
    useEffect(() => {
        fetch('/api/vet/login').then(r => r.json()).then(setData).then(() => console.log(data))
    })

    return (
        <div>
            <p>inicio d sesión</p>
            <SessionCard name="Lol" route="/" id={"1"}/>
        </div>
    )
}