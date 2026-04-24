import { getNameFromJWT } from "@/lib/jwtService";
import { NextRequest } from "next/server";

export async function GET(req: NextRequest) {
    return getNameFromJWT(req)
}