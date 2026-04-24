import ObjectViewer from "@/components/objectViewer";
import { Cita } from "@/interfaces/requests/dateRequest";
import { Owner } from "@/interfaces/requests/ownerRequest";
import { Pet } from "@/interfaces/requests/petRequest";
import { Vaccine } from "@/interfaces/requests/vaccineRequest";
import { Vet } from "@/interfaces/requests/vetRequest";
import { emptyCita, emptyOwner, emptyPet, emptyVaxx, emptyVet } from "@/lib/constants";

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