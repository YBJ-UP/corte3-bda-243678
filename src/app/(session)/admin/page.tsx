"use client"

import ObjectEditor from "@/components/objectEditor";
import ObjectViewer from "@/components/objectViewer";
import { Cita } from "@/interfaces/requests/dateRequest";
import { Owner } from "@/interfaces/requests/ownerRequest";
import { Pet } from "@/interfaces/requests/petRequest";
import { Vaccine } from "@/interfaces/requests/vaccineRequest";
import { Vet } from "@/interfaces/requests/vetRequest";
import { emptyCita, emptyOwner, emptyPet, emptyVaxx, emptyVet, tablas } from "@/lib/constants";
import { useState } from "react";

export default function Admin() {
    const [ editorOpen, setEditorOpen ] = useState<boolean>(false)

    return (
        <section>
            <section>
                <h2 className="text-2xl">OPCIONES:</h2>
                <button type="button" onClick={() => setEditorOpen(true)}>Editar datos</button>
                <ObjectEditor
                    objects={[tablas.OWNER, tablas.VET, tablas.PET, tablas.DATE, tablas.VAXX]}
                    isOpen={editorOpen}
                    onClose={() => setEditorOpen(false)}
                />
            </section>
            <section className="flex flex-col gap-10">
                <h3 className="text-2xl">DATOS:</h3>
                <ObjectViewer<Required<Owner>> object={emptyOwner} name="owner" alias="Dueños" />
                <ObjectViewer<Required<Pet>> object={emptyPet} name="pet" alias="Mascotas" />
                <ObjectViewer<Required<Vet>> object={emptyVet} name="vet" alias="Veterinarios" />
                <ObjectViewer<Required<Cita>> object={emptyCita} name="date" alias="Citas agendadas" />
                <ObjectViewer<Required<Vaccine>> object={emptyVaxx} name="vaccine" alias="Vacunas" />
            </section>
        </section>
    )
}