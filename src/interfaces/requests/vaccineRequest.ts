import z from "zod"

export const VaccineSchema = z.object({
    id: z.number().int(),
    nombre: z.string().max(80),
    stock_actual: z.number().int().gte(0).default(0),
    stock_minimo: z.number().int().gt(0).default(5),
    costo_unitario: z.number()
})

export const VaccinePostSchema = z.object({
    nombre: z.string().max(80),
    stock_actual: z.number().int().gte(0).default(0),
    stock_minimo: z.number().int().gt(0).default(5),
    costo_unitario: z.number()
})

export const VaccinePatchSchema = z.object({
    nombre: z.string().max(80).optional(),
    stock_actual: z.number().int().gte(0).optional(),
    stock_minimo: z.number().int().gt(0).optional(),
    costo_unitario: z.number().optional()
})

export type Vaccine = z.infer<typeof VaccineSchema>
export type VaccinePost = z.infer<typeof VaccinePostSchema>
export type VaccinePatch = z.infer<typeof VaccinePatchSchema>