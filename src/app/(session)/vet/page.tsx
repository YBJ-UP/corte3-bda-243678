"use client"

import ObjectEditor from "@/components/objectEditor";
import ObjectViewer from "@/components/objectViewer";
import { Cita } from "@/interfaces/requests/dateRequest";
import { Pet } from "@/interfaces/requests/petRequest";
import { Vaccine } from "@/interfaces/requests/vaccineRequest";
import { emptyCita, emptyPet, emptyVaxx, tablas } from "@/lib/constants";
import { useState } from "react";

export default function Vet() {
    const [ editorOpen, setEditorOpen ] = useState<boolean>(false)
    return (
        <section>
            <section>
                    <button type="button" onClick={() => setEditorOpen(true)} className="px-15 py-3 bg-green-600 rounded-2xl">Editar datos</button>
                    <ObjectEditor
                        objects={[tablas.PET, tablas.DATE]}
                        permission={["add", "edit"]}
                        isOpen={editorOpen}
                        onClose={() => setEditorOpen(false)}
                    />
            </section>
            <section className="flex flex-col gap-10">
                <h3 className="text-2xl">DATOS:</h3>
                <ObjectViewer<Required<Pet>> object={emptyPet} name="pet" alias="Mascotas registradas" />
                <ObjectViewer<Required<Cita>> object={emptyCita} name="date" alias="Citas agendadas" />
                <ObjectViewer<Required<Vaccine>> object={emptyVaxx} name="date" alias="Citas agendadas" />
            </section>
        </section>
            
    )
}