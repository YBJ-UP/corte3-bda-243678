"use client"

import { useEffect, useState } from "react"

interface objectViewProps<T extends object> {
    object: T
    name: string
    alias: string
}

export default function ObjectViewer<T extends object>(props: objectViewProps<T>) {
    const llaves = Object.keys(props.object)
    const [ data, setData ] = useState<T[]>([])
    const [loading, setIsLoading] = useState<boolean>(false)

    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsLoading(true)
                const res = await fetch(`/api/${props.name}`)
                const json = await res.json()
                setData(json.data)
            } catch {
                console.error("XD")
            } finally {
                setIsLoading(false)
            }
        }
        fetchData()
    }, [])

    return (
        <div>
            <h1>{props.alias}</h1>
            <div className="flex gap-5">
                {llaves.map((key) => (
                    <p key={key}>{key.toUpperCase()}</p>
                ))}
            </div>
            
        </div>
    )
}