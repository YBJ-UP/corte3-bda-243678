import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col gap-5">
      <Link href={"/admin"}>Admin</Link>
      <Link href={"/recep"}>Recepción</Link>
      <Link href={"/vet"}>Veterinario</Link>
    </div>
  );
}
