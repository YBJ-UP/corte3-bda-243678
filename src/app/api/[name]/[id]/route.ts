import { get, patch, remove } from "@/lib/apiClient"
import { getPatchType, getType } from "@/utils/typeUtils"
import { NextRequest, NextResponse } from "next/server"

export async function GET(req: NextRequest, { params }: { params: { name: string, id: number } }) {
    try {
        const { name, id } = await params
        const typeObj = getType(name)
        type reqT = typeof typeObj
        const data = await get<reqT>(`/${name}/${id}`, req)
        return NextResponse.json(data)
    } catch (e) {
        return NextResponse.json({ message: e.message }, { status: 500 })
    }
}

export async function PATCH(req: NextRequest, { params }: { params: { name: string, id: number } }) {
    try {
        const { name, id } = await params
        
        const typeObj = getType(name)
        type reqT = typeof typeObj
        
        const patchObj = getPatchType(name)
        type patchT = typeof patchObj
        
        const body = await req.body as patchT

        const data = await patch<reqT, patchT>(`/${name}/${id}`, req, body)
        return NextResponse.json(data)
    } catch (e) {
        return NextResponse.json({ message: e.message }, { status: 500 })
    }
}

export async function DELETE(req: NextRequest, { params }: { params: { name: string, id: number } }) {
    try {
        const { name, id } = await params
        const data = await remove(`/${name}/${id}`, req)
        return NextResponse.json(data)
    } catch (e) {
        return NextResponse.json({ message: e.message }, { status: 500 })
    }
}