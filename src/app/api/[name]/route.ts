import { get } from "@/lib/apiClient";
import { NextRequest, NextResponse } from "next/server";

function getType(name: string) {
    switch (name){
        case "": return
        default: return
    }
}

export async function GET(req: NextRequest, { params }: { params: { name: string } }) {
    try {
        const data = await get<unknown>(`/${params.name}`, req)
        return NextResponse.json(data)
    } catch (e) {
        return NextResponse.json({ message: e.message }, { status: 500 })
    }
}