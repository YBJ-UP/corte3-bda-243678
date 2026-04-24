"use client"

import { useEffect, useState } from "react"

interface objectViewProps<T extends object & { id: number }> {
    object: T
    name: string
    alias: string
}

export default function ObjectViewer<T extends object & { id: number }>(props: objectViewProps<T>) {
    const llaves = Object.keys(props.object)
    const [ data, setData ] = useState<T[]>([])
    const [ errMsg, setErr ] = useState<string>()
    const [loading, setIsLoading] = useState<boolean>(false)
    const [ isOpen, setIsOpen ] = useState<boolean>(false)

    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsLoading(true)
                const res = await fetch(`/api/${props.name}`)
                const json = await res.json()
                setData(json.data)
                setErr("")
            } catch {
                console.error("No se pudieron obtener los datos correctamente.")
                setErr("No se pudieron obtener los datos correctamente.")
            } finally {
                setIsLoading(false)
            }
        }
        fetchData()
    }, [])

    return (
        <section>
            <div className="flex gap-20 items-center mb-2">
                <h2 className="text-xl">{props.alias}</h2>
                <button
                    type="button"
                    onClick={() => setIsOpen(!isOpen)}
                    className="px-10 py-2 bg-emerald-500 rounded-2xl"
                >
                    {isOpen ? "Cerrar" : "Ver"}
                </button>
            </div>

            <section>
                {!isOpen && (
                    <p>------------------------------------------------------------</p>
                ) || (
                    <div>
                        <div className="grid grid-cols-7">
                            {llaves.map((key) => (
                                <p key={key}>{key.toUpperCase()}</p>
                            ))}
                        </div>
                        {loading && (
                            <p className="text-xl font-semibold">Cargando...</p>
                        )}
                        {errMsg && (
                            <p>{errMsg}</p>
                        )}
                        {!errMsg && data && !loading && (
                            <>
                                {data.map((obj) => (
                                    <div key={obj.id} className="grid grid-cols-7 my-1">
                                        {Object.entries(obj).map(([key, atr]) => (
                                            <span key={key}>{String(atr ?? "-")}</span>
                                        ))}
                                    </div>
                                ))}
                            </>
                        )}
                    </div>
                    
                )}
                
            </section>
        </section>
    )
}