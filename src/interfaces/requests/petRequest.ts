import z from "zod"

export const PetSchema = z.object({
    id: z.number().int(),
    nombre: z.string().max(50),
    especie: z.string().max(30),
    fecha_nacimiento: z.coerce.date(),
    dueno_id: z.number().int()
})

export const PetPostSchema = z.object({
    nombre: z.string().max(50),
    especie: z.string().max(30),
    fecha_nacimiento: z.coerce.date().optional(),
    dueno_id: z.number().int()
})

export const PetPatchSchema = z.object({
    nombre: z.string().max(50).optional(),
    especie: z.string().max(30).optional(),
    fecha_nacimiento: z.coerce.date().optional(),
    dueno_id: z.number().int().optional()
})

export type Pet = z.infer<typeof PetSchema>
export type PetPost = z.infer<typeof PetPostSchema>
export type PetPatch = z.infer<typeof PetPatchSchema>