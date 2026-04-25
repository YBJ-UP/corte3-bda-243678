import { get } from "@/lib/apiClient";
import { getType } from "@/utils/typeUtils";
import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest, { params }: { params: { name: string, search: string } }) {
    try {
        const { name, search } = await params
        const typeObj = getType(name)
        type reqT = (typeof typeObj)[]
        const data = await get<reqT>(`/${name}/search/${search}`, req)
        return NextResponse.json(data)
    } catch (e) {
        return NextResponse.json({ message: e.message }, { status: 500 })
    }
}