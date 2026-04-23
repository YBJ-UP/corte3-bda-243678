interface objectViewProps<T extends object> {
    object: T
}

export default function ObjectViewer<T extends object>(props: objectViewProps<T>) {
    const llaves = Object.keys(props.object)
    return (
        <div>
            <div className="flex gap-5">
                {llaves.map((key) => (
                    <p key={key}>{key.toUpperCase()}</p>
                ))}
            </div>
            
        </div>
    )
}