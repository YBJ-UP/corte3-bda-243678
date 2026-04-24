import ObjectViewer from "@/components/objectViewer";
import { Cita } from "@/interfaces/requests/dateRequest";
import { Owner } from "@/interfaces/requests/ownerRequest";
import { Pet } from "@/interfaces/requests/petRequest";
import { emptyCita, emptyOwner, emptyPet } from "@/lib/constants";

export default function Reception() {
    return (
        <div>
            <ObjectViewer<Required<Owner>> object={emptyOwner} name="owner" alias="Dueños" />
            <ObjectViewer<Required<Cita>> object={emptyCita} name="date" alias="Citas agendadas" />
            <ObjectViewer<Required<Pet>> object={emptyPet} name="date" alias="Mascotas registradas" />
        </div>
    )
}