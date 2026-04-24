import { Owner } from "@/interfaces/requests/ownerRequest";
import { Vet } from "@/interfaces/requests/vetRequest";
import { get } from "@/lib/apiClient";
import { NextRequest, NextResponse } from "next/server";

function getType(name: string) {
    switch (name){
        case "owner": return { nombre: "" } as Owner
        case "vet": return { nombre: "" } as Vet
        case "pet": return { nombre: "" } as Owner
        case "date": return { nombre: "" } as Owner
        case "vaccine": return { nombre: "" } as Owner
        default: return null
    }
}

export async function GET(req: NextRequest, { params }: { params: { name: string } }) {
    try {
        console.log(await params.name)
        console.log(params.name)
        const { name } = await params
        const data = await get<unknown>(`/${name}`, req)
        return NextResponse.json(data)
    } catch (e) {
        return NextResponse.json({ message: e.message }, { status: 500 })
    }
}