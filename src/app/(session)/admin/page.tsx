import ObjectViewer from "@/components/tableViewer";
import { Owner } from "@/interfaces/requests/ownerRequest";

const emptyOwner: Owner = { id:0, nombre:"", telefono:"", email:"" } // solo para sacarle las llaves

export default function Admin() {
    return (
        <div>
            <p>intento</p>
            <ObjectViewer<Owner> object={emptyOwner} />
        </div>
    )
}