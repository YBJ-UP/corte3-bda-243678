import SessionCard from "@/components/session_card";

export default function Home() {
  return (
    <section className="flex justify-center items-center gap-25 my-auto">
    <div>
      <h1 className="text-2xl font-extrabold">¡Bienvenido a TuxMascotas!</h1>
      <h2 className="text-xl font-semibold">Inicie sesión como:</h2>
    </div>
      <section className="flex flex-col gap-5 w-50">
        <SessionCard name="Admin" route="/admin" />
        <SessionCard name="Recepción" route="/recep" />
        <SessionCard name="Veterinarios" route="/vet" />
      </section>
    </section>
  );
}
