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
    const [selectedId, setSelectedId] = useState<number | null>(null)
    const [formValues, setFormValues] = useState<Record<string, string>>({})
    const selectedObj = selectedTableObj?.find(row => row.id === selectedId) ?? null

    function handleSelectRow(row: Owner | Vet | Pet | Cita | Vaccine) {
        setSelectedId(row.id)
        const values: Record<string, string> = {}
        Object.entries(row).forEach(([key, val]) => {
            values[key] = String(val ?? "")
        })
        setFormValues(values)
        console.log(values)
    }

    async function setSelectionObj(selection: tabla) {
        setCurrentSelect(selection.attributes)
        setCurrentObjName(selection.name)

        if (action === "Editar" || action === "Eliminar") {
            try {
                const response = await fetch(`/api/${selection.name}`)
                if (!response.ok) {
                    console.error("No se pudo extrar la información del servidor")
                }
                const json = await response.json()
                setSelectedTableObj(json.data as Owner[] | Vet[] | Pet[] | Cita[] | Vaccine[])
            } catch(e: any) {
                console.error("Error: ", e.message)
            }
        } else {
            setSelectedTableObj(null)
            setFormValues({})
        }
    }

    async function getEditInfo(action: "Añadir" | "Eliminar" | "Editar") {
        setAction(action)
        if (action === "Editar") {
            try {
                const response = await fetch(`/api/${currentObjName}`)
                if (!response.ok) {
                    console.error("No se pudo extrar la información del servidor")
                }
                const json = await response.json()
                setSelectedTableObj(json.data as Owner[] | Vet[] | Pet[] | Cita[] | Vaccine[])
            } catch(e: any) {
                console.error("Error: ", e.message)
            }
        }
        if (action === "Añadir") {
            setSelectedTableObj(null)
            setFormValues({})
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

                            <div>
                                {(action === "Editar" || action === "Eliminar") && selectedTableObj && (
                                    <div className="flex flex-col gap-2 bg-gray-800 p-5 rounded-2xl max-h-60 overflow-y-auto">
                                        <p className="font-bold">Selecciona un registro:</p>
                                        {selectedTableObj.map((row) => (
                                            <button
                                                key={row.id}
                                                type="button"
                                                className={`text-left px-4 py-2 ${row.id === selectedId ? "bg-green-950 hover:bg-green-900" : "hover:bg-gray-700 rounded"}`}
                                                onClick={() => handleSelectRow(row)}
                                            >
                                                ID: {row.id} { row.nombre ? `Nombre: ${row.nombre}` : `Motivo: ${row.motivo}` }
                                            </button>
                                        ))}
                                    </div>
                                )}

                                {action !== "Eliminar" && (
                                    <div>
                                        <ol className="grid grid-cols-3 gap-5">
                                            {currentSelect
                                                .filter(attr => attr !== "id")
                                                .map((attr) => (
                                                    <li key={attr} className="flex flex-col">
                                                        <span>{attr.toLocaleUpperCase()}</span>
                                                        <input
                                                            type="text"
                                                            name={attr}
                                                            placeholder={selectedObj ? String(selectedObj[attr as keyof typeof selectedObj] ?? "") : attr}
                                                            onChange={(e) => setFormValues(prev => ({
                                                                ...prev,
                                                                [attr]: e.target.value
                                                            }))}
                                                        />
                                                    </li>
                                                ))
                                            }
                                        </ol>
                                    </div>
                                )}
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