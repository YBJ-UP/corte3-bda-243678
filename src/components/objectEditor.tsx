"use client"

import { tabla } from "@/lib/constants"
import { useState } from "react"

interface ObjectEditorProps {
    objects: tabla[]
    isOpen: boolean
    onClose: () => void
}

export default function ObjectEditor(props: ObjectEditorProps) {
    const [ currentSelect, setCurrentSelect ] = useState<string[]>([])
    const [ action, setAction ] = useState<"Añadir" | "Eliminar" | "Editar">("Añadir")
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
                                            if (selected) setCurrentSelect(selected.attributes)
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
                                        onChange={(e) => setAction(e.target.value as "Añadir" | "Editar" | "Eliminar")}
                                    >
                                        <option value="Añadir">Añadir</option>
                                        <option value="Editar">Editar</option>
                                        <option value="Eliminar">Eliminar</option>
                                    </select>
                                </div>
                            </div>

                            <div>
                                <ol>
                                    {currentSelect.map((attr, key:  number) => (
                                        <li key={key}>
                                            <span>{attr}</span>
                                            <input type="text" name={attr} id={String(key)} placeholder={attr} />
                                        </li>
                                    ))}
                                </ol>
                            </div>
                            
                            <div>
                                <p>Acción:</p>
                                <p>{action}</p>
                            </div>

                            <button type="button" onClick={props.onClose} className="px-15 py-3 bg-red-700 hover:bg-red-600 rounded-2xl">Cerrar</button>
                        </div>
                        
                    </div>
                </section>
            )}
        </>
        
        
    )
}