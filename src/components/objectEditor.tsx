import { tabla } from "@/lib/constants"

interface ObjectEditorProps {
    objects: tabla[]
    isOpen: boolean
    onClose: () => void
}

export default function ObjectEditor(props: ObjectEditorProps) {
    return (
        <>
            {props.isOpen && (
                <section className="w-full h-full fixed inset-0">
                    <div className="bg-emerald-300 opacity-10 h-full w-full"></div>
                    <div className="absolute inset-0 flex flex-col gep-5 justify-center items-center h-full">
                        <select name="ObjSelector" id="lol" className="bg-gray-800">
                            {props.objects.map((obj) => (
                                <option key={obj.name} value={obj.name}>{obj.alias}</option>
                            ))}
                            </select>
                        <button type="button" onClick={props.onClose}>Cerrar</button>
                    </div>
                </section>
            )}
        </>
        
        
    )
}