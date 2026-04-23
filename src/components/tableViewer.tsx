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

    useEffect(() => {
        fetch(`/api/${props.name}`).then(r => r.json()).then(setData).then( () => console.log(data) )
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