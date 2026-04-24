import { get } from "@/lib/apiClient";
import { NextRequest, NextResponse } from "next/server";

export interface VetProfile {
    id: number
    nombre: string
}

export async function GET(req: NextRequest) {
    try {
        const data = await get<VetProfile[]>('/veterinarios', req)
    } catch (e) {
        return NextResponse.json({ message: e.message }, { status: 500 })
    }
}