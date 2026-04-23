import Link from "next/link";

export default function Layout({
        children,
    }: Readonly<{
        children: React.ReactNode;
}>){
    return (
        <>
            <div className="flex items-center justify-between bg-green-700 py-7 px-15">
                <p className="text-xl font-bold">Veterinaria TuxMascotas</p>
                <Link href={"/"} className="font-medium hover:font-bold">Cerrar sesión</Link>
            </div>
            {children}
        </>
    )
}