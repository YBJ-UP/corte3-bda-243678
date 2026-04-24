import { Vet } from "@/interfaces/requests/vetRequest";
import { get } from "@/lib/apiClient";
import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
    try {
        const data = await get<Vet[]>('/veterinarios', req)
    } catch (e) {
        return NextResponse.json({ message: e.message }, { status: 500 })
    }
}