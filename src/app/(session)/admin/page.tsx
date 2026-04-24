import ObjectViewer from "@/components/objectViewer";
import { Owner } from "@/interfaces/requests/ownerRequest";
import { Vet } from "@/interfaces/requests/vetRequest";

const emptyOwner: Required<Owner> = { id:0, nombre:"", telefono:"", email:"" } // solo para sacarle las llaves
const emptyVet: Required<Vet> = { id:0, nombre:"", cedula:"", dias_descanso:"", activo: false } // solo para sacarle las llaves

export default function Admin() {

    return (
        <div>
            <section className="flex flex-col gap-10">
                <ObjectViewer<Required<Owner>> object={emptyOwner} name="owner" alias="Dueños" />
                <ObjectViewer<Required<Vet>> object={emptyVet} name="vet" alias="Veterinarios" />
            </section>
        </div>
    )
}