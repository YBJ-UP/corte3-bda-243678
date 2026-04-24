import z from "zod";

const ownerGet = z.object({
    id: z.int().positive(),
    nombre: z.string().max(100),
    telefono: z.string().max(20).optional(),
    email: z.string().max(100).optional()
})
export type Owner = z.infer<typeof ownerGet>

const ownerPost = z.object({
    nombre: z.string().max(100),
    telefono: z.string().max(20).optional(),
    email: z.string().max(100).optional()
})

export type OwnerPost = z.infer<typeof ownerPost>

const ownerPatch = z.object({
    nombre: z.string().max(100).optional(),
    telefono: z.string().max(20).optional(),
    email: z.string().max(100).optional()
})

export type OwnerPatch = z.infer<typeof ownerPatch>