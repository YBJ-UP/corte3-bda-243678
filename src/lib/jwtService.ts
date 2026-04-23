import jwt from 'jsonwebtoken'

export function generateToken(role: "a" | "v" | "r", id: number) {
    const token = jwt
}