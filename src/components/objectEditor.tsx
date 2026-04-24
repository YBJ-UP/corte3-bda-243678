"use client"

import { Cita } from "@/interfaces/requests/dateRequest"
import { Owner } from "@/interfaces/requests/ownerRequest"
import { Pet } from "@/interfaces/requests/petRequest"
import { Vaccine } from "@/interfaces/requests/vaccineRequest"
import { Vet } from "@/interfaces/requests/vetRequest"
import { tabla } from "@/lib/constants"
import { useState } from "react"

interface ObjectEditorProps {
    objects: tabla[]
    isOpen: boolean
    onClose: () => void
}

export default function ObjectEditor(props: ObjectEditorProps) {
    const [ currentSelect, setCurrentSelect ] = useState<string[]>(props.objects[0].attributes)
    const [ currentObjName, setCurrentObjName ] = useState<string>(props.objects[0].name)
    const [ selectedTableObj, setSelectedTableObj ] = useState<Owner[] | Vet[] | Pet[] | Cita[] | Vaccine[] | null>(null)
    const [ action, setAction ] = useState<"Añadir" | "Eliminar" | "Editar">("Añadir")

    function setSelectionObj(selection: tabla) {
        setCurrentSelect(selection.attributes)
        setCurrentObjName(selection.name)
    }

    async function getEditInfo(action: "Añadir" | "Eliminar" | "Editar") {
        setAction(action)
        if (action === "Editar") {
            try {
                const response = await fetch(`/api/${currentObjName}`)
                if (!response.ok) {
                    console.error("No se pudo extrar la información del servidor")
                }
                const json = await response.json() as Owner[] | Vet[] | Pet[] | Cita[] | Vaccine[]
                setSelectedTableObj(json)
            } catch(e: any) {
                console.error("Error: ", e.message)
            }
        }
    }

    return (
        <>
            {props.isOpen && (
                <section className="w-full h-full fixed inset-0">
                    <div className="bg-emerald-300 opacity-10 h-full w-full"></div>
                    <div className="absolute inset-0 flex flex-col gep-5 justify-center items-center h-full">

                        <div className="flex flex-col gap-10 items-center justify-center bg-gray-900 p-15 rounded-2xl">

                            <div className="flex flex-col gap-5 bg-gray-800 px-10 py-5 rounded-2xl">
                                <div className="flex gap-5">
                                    <p>Seleccionar tabla: </p>
                                    <select
                                        name="objSelector"
                                        className="bg-gray-800"
                                        onChange={(e) => {
                                            const selected = props.objects.find(obj => obj.name === e.target.value)
                                            if (selected) setSelectionObj(selected)
                                        }}
                                    >
                                        {props.objects.map((obj) => (
                                            <option key={obj.name} value={obj.name}>{obj.alias}</option>
                                        ))}
                                    </select>
                                </div>
                                <div className="flex gap-5">
                                    <p>Acción</p>
                                    <select
                                        name="actionSelector"
                                        className="bg-gray-800"
                                        onChange={(e) => getEditInfo(e.target.value as "Añadir" | "Eliminar" | "Editar")}
                                    >
                                        <option value="Añadir">Añadir</option>
                                        <option value="Editar">Editar</option>
                                        <option value="Eliminar">Eliminar</option>
                                    </select>
                                </div>
                            </div>

                            {selectedTableObj && (
                                <div>
                                    {selectedTableObj.map((row) => (
                                        <p>{row.id}</p>
                                    ))}
                                </div>
                            )}

                            <div>
                                <ol className="grid grid-cols-3 gap-5">
                                    {currentSelect.map((attr, key:  number) => (
                                        <li key={key} className="flex flex-col">
                                            <span>{attr.toLocaleUpperCase()}</span>
                                            <input type="text" name={attr} id={String(key)} placeholder={attr} />
                                        </li>
                                    ))}
                                </ol>
                            </div>
                            
                            <div className="bg-gray-700 px-15 py-5 rounded-2xl">
                                <p>Acción:</p>
                                <p className="font-bold">{action}</p>
                            </div>

                            <button type="button" onClick={props.onClose} className="px-15 py-3 bg-red-700 hover:bg-red-600 rounded-2xl">Cerrar</button>
                        </div>
                        
                    </div>
                </section>
            )}
        </>
        
        
    )
}