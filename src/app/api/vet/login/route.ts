import { unprotectedRequest } from "@/lib/apiClient";
import { NextRequest, NextResponse } from "next/server";

export interface VetProfile {
    id: number
    nombre: string
}

export async function GET(req: NextRequest) {
    try {
        const data = await unprotectedRequest<VetProfile[]>()
        return NextResponse.json(data)
    } catch (e) {
        return NextResponse.json({ message: e.message }, { status: 500 })
    }
}