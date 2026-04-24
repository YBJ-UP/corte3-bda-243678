import z from "zod";

const vetGet = z.object({
    id: z.int().positive(),
    nombre: z.string().max(100),
    cedula: z.string().max(20),
    dias_descanso: z.string().max(50),
    activo: z.boolean().default(true)
})
export type Vet = z.infer<typeof vetGet>

const vetPost = z.object({
    nombre: z.string().max(100),
    cedula: z.string().max(20),
    dias_descanso: z.string().max(50),
    activo: z.boolean().default(true)
})

export type VetPost = z.infer<typeof vetPost>

const vetPatch = z.object({
    nombre: z.string().max(100).optional(),
    cedula: z.string().max(20).optional(),
    dias_descanso: z.string().max(50).optional(),
    activo: z.boolean().default(true).optional()

})

export type VetPatch = z.infer<typeof vetPatch>