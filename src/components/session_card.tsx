import Link from "next/link"

interface SessionCardProps {
    name: string
    route: string
    id: string | null
}

export default function SessionCard(data: SessionCardProps) {
    return (
        <Link href={data.route} className="px-10 py-5 bg-cyan-600 rounded-2xl hover:bg-cyan-500 hover:font-bold hover:scale-110">
            <p className="text-xl">{data.name}</p>
        </Link>
    )
}