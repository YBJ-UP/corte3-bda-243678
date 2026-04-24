import { get, post } from "@/lib/apiClient";
import { getPostType, getType } from "@/utils/typeUtils";
import { NextRequest, NextResponse } from "next/server";

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

export async function POST(req: NextRequest, { params }: { params: { name: string } }) {
    try {
        const { name } = await params
        
        const typeObj = getType(name)
        type reqT = typeof typeObj
        
        const postObj = getPostType(name)
        type postT = typeof postObj
        
        const body = await req.body as postT

        const data = await post<reqT, postT>(`/${name}`, req, body)
        return NextResponse.json(data)
    } catch (e) {
        return NextResponse.json({ message: e.message }, { status: 500 })
    }
}