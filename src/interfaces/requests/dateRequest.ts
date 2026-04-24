import z from "zod"

const EstadoSchema = z.enum(["AGENDADA", "COMPLETADA", "CANCELADA"])

export const DateSchema = z.object({
    id: z.number().int(),
    mascota_id: z.number().int(),
    veterinario_id: z.number().int(),
    fecha_hora: z.coerce.date(),
    motivo: z.string(),
    costo: z.number(),
    estado: EstadoSchema.default("AGENDADA")
})

export const DatePostSchema = z.object({
    mascota_id: z.number().int(),
    veterinario_id: z.number().int(),
    fecha_hora: z.coerce.date(),
    motivo: z.string().optional(),
    costo: z.number().optional(),
    estado: EstadoSchema.default("AGENDADA")
})

export const DatePatchSchema = z.object({
    mascota_id: z.number().int().optional(),
    veterinario_id: z.number().int().optional(),
    fecha_hora: z.coerce.date().optional(),
    motivo: z.string().optional(),
    costo: z.number().optional(),
    estado: EstadoSchema.optional()
})

export type Cita = z.infer<typeof DateSchema>
export type CitaPost = z.infer<typeof DatePostSchema>
export type CitaPatch = z.infer<typeof DatePatchSchema>