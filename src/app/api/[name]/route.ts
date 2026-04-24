import { Cita } from "@/interfaces/requests/dateRequest";
import { Owner } from "@/interfaces/requests/ownerRequest";
import { Pet } from "@/interfaces/requests/petRequest";
import { Vaccine } from "@/interfaces/requests/vaccineRequest";
import { Vet } from "@/interfaces/requests/vetRequest";
import { get } from "@/lib/apiClient";
import { NextRequest, NextResponse } from "next/server";

function getType(name: string) {
    switch (name){
        case "owner": return { nombre: "" } as Owner
        case "vet": return { nombre: "" } as Vet
        case "pet": return { nombre: "" } as Pet
        case "date": return { motivo: "" } as Cita
        case "vaccine": return { nombre: "" } as Vaccine
        default: return null
    }
}

export async function GET(req: NextRequest, { params }: { params: { name: string } }) {
    try {
        const { name } = await params
        const typeObj = getType(name)
        type reqT = typeof typeObj
        const data = await get<reqT>(`/${name}`, req)
        return NextResponse.json(data)
    } catch (e) {
        return NextResponse.json({ message: e.message }, { status: 500 })
    }
}