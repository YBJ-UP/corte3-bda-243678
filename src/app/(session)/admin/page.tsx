import ObjectViewer from "@/components/tableViewer";
import { Owner } from "@/interfaces/requests/ownerRequest";
import { Vet } from "@/interfaces/requests/vetRequest";

const emptyOwner: Owner = { id:0, nombre:"", telefono:"", email:"" } // solo para sacarle las llaves
const emptyVet: Vet = { id:0, nombre:"", cedula:"", dias_descanso:"", activo: false } // solo para sacarle las llaves

export default function Admin() {
    return (
        <div>
            <p>intento</p>
            <ObjectViewer<Owner> object={emptyOwner} name="owner" alias="Dueños" />
            <ObjectViewer<Vet> object={emptyVet} name="vet" alias="Veterinarios" />
        </div>
    )
}