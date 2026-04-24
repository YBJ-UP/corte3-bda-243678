import ObjectViewer from "@/components/objectViewer";
import { Cita } from "@/interfaces/requests/dateRequest";
import { Owner } from "@/interfaces/requests/ownerRequest";
import { Pet } from "@/interfaces/requests/petRequest";
import { Vaccine } from "@/interfaces/requests/vaccineRequest";
import { Vet } from "@/interfaces/requests/vetRequest";

const emptyOwner: Required<Owner> = { id:0, nombre:"", telefono:"", email:"" } // solo para sacarle las llaves
const emptyVet: Required<Vet> = { id:0, nombre:"", cedula:"", dias_descanso:"", activo: false } // solo para sacarle las llaves
const emptyPet: Required<Pet> = { id:0, nombre:"", especie:"", fecha_nacimiento: new Date(), dueno_id: 0  } // solo para sacarle las llaves
const emptyCita: Required<Cita> = { id:0, mascota_id:0, veterinario_id: 0, fecha_hora: new Date(), motivo:"", costo: 0, estado: "CANCELADA" } // solo para sacarle las llaves
const emptyVaxx: Required<Vaccine> = { id:0, nombre:"", stock_actual:0, stock_minimo:0, costo_unitario:0  } // solo para sacarle las llaves

export default function Admin() {

    return (
        <div>
            <section className="flex flex-col gap-10">
                <ObjectViewer<Required<Owner>> object={emptyOwner} name="owner" alias="Dueños" />
                <ObjectViewer<Required<Pet>> object={emptyPet} name="pet" alias="Mascotas" />
                <ObjectViewer<Required<Vet>> object={emptyVet} name="vet" alias="Veterinarios" />
                <ObjectViewer<Required<Cita>> object={emptyCita} name="date" alias="Citas agendadas" />
                <ObjectViewer<Required<Vaccine>> object={emptyVaxx} name="vaccine" alias="Vacunas" />
            </section>
        </div>
    )
}