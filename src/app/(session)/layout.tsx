import Link from "next/link";

export default function Layout({
        children,
    }: Readonly<{
        children: React.ReactNode;
}>){
    return (
        <>
            <div>
                <p>Veterinaria TuxMascotas</p> //es lo que se me ocurrió, no lo pensé mucho
                <Link href={"/"}>Cerrar sesión</Link>
            </div>
            {children}
        </>
    )
}