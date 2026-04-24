import ObjectViewer from "@/components/objectViewer";
import { Cita } from "@/interfaces/requests/dateRequest";
import { Owner } from "@/interfaces/requests/ownerRequest";
import { Pet } from "@/interfaces/requests/petRequest";
import { emptyCita, emptyOwner, emptyPet } from "@/lib/constants";

export default function Vet() {
    return (
        <section>
            <section>
                <h2>OPCIONES</h2>
            </section>
            <section className="flex flex-col gap-10">
                <h3 className="text-2xl">DATOS:</h3>
                <ObjectViewer<Required<Owner>> object={emptyOwner} name="owner" alias="Dueños" />
                <ObjectViewer<Required<Pet>> object={emptyPet} name="pet" alias="Mascotas registradas" />
                <ObjectViewer<Required<Cita>> object={emptyCita} name="date" alias="Citas agendadas" />
            </section>
        </section>
            
    )
}