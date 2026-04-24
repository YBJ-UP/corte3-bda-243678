import { Cita, CitaPatch, CitaPost } from "@/interfaces/requests/dateRequest"
import { Owner, OwnerPatch, OwnerPost } from "@/interfaces/requests/ownerRequest"
import { Pet, PetPatch, PetPost } from "@/interfaces/requests/petRequest"
import { Vaccine, VaccinePatch, VaccinePost } from "@/interfaces/requests/vaccineRequest"
import { Vet, VetPatch, VetPost } from "@/interfaces/requests/vetRequest"

export function getType(name: string) { // tambien para delete
    switch (name){
        case "owner": return { nombre: "" } as Owner
        case "vet": return { nombre: "" } as Vet
        case "pet": return { nombre: "" } as Pet
        case "date": return { motivo: "" } as Cita
        case "vaccine": return { nombre: "" } as Vaccine
        default: return null
    }
}

export function getPostType(name: string) {
    switch (name){
        case "owner": return { nombre: "" } as OwnerPost
        case "vet": return { nombre: "" } as VetPost
        case "pet": return { nombre: "" } as PetPost
        case "date": return { motivo: "" } as CitaPost
        case "vaccine": return { nombre: "" } as VaccinePost
        default: return null
    }
}

export function getPatchType(name: string) {
    switch (name){
        case "owner": return { nombre: "" } as OwnerPatch
        case "vet": return { nombre: "" } as VetPatch
        case "pet": return { nombre: "" } as PetPatch
        case "date": return { motivo: "" } as CitaPatch
        case "vaccine": return { nombre: "" } as VaccinePatch
        default: return null
    }
}