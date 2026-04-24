import { generateToken } from "@/lib/jwtService"

export async function POST(req: Request) {
    const { name, role, id } = await req.json()

    return generateToken(name, role, id)
}