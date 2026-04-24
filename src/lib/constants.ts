import { Cita } from "@/interfaces/requests/dateRequest"
import { Owner } from "@/interfaces/requests/ownerRequest"
import { Pet } from "@/interfaces/requests/petRequest"
import { Vaccine } from "@/interfaces/requests/vaccineRequest"
import { Vet } from "@/interfaces/requests/vetRequest"

export const emptyOwner: Required<Owner> = { id:0, nombre:"", telefono:"", email:"" } // solo para sacarle las llaves
export const emptyVet: Required<Vet> = { id:0, nombre:"", cedula:"", dias_descanso:"", activo: false } // solo para sacarle las llaves
export const emptyPet: Required<Pet> = { id:0, nombre:"", especie:"", fecha_nacimiento: new Date(), dueno_id: 0  } // solo para sacarle las llaves
export const emptyCita: Required<Cita> = { id:0, mascota_id:0, veterinario_id: 0, fecha_hora: new Date(), motivo:"", costo: 0, estado: "CANCELADA" } // solo para sacarle las llaves
export const emptyVaxx: Required<Vaccine> = { id:0, nombre:"", stock_actual:0, stock_minimo:0, costo_unitario:0  } // solo para sacarle las llaves