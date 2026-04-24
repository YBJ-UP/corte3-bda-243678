import { generateToken } from "@/lib/jwtService"

export async function POST(req: Request) {
    const { role, id } = await req.json()

    return generateToken(role, id)
}