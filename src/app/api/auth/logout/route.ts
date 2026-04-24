import { destroyToken } from "@/lib/jwtService";
import { NextRequest } from "next/server";

export async function POST(req: NextRequest) {
    return destroyToken()
}