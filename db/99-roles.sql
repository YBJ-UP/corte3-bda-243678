-- 3 ROLES - VETERINARIO, RECEPCION Y ADMINISTRADORES

-- Veterinario
-- Solo ve las mascotas que él atiende (según vet_atiende_mascota). Puede registrar nuevas citas y
-- aplicar vacunas a sus mascotas. No puede ver historial médico de mascotas que no atiende.

-- Recepción
-- Ve todas las mascotas y sus dueños (datos de contacto). Puede agendar citas para cualquier mascota.
-- No puede ver vacunas aplicadas (información médica).

-- Administrador
-- Ve todo. Puede crear usuarios, asignar mascotas a veterinarios, y gestionar inventario de vacunas.

DROP ROLE IF EXISTS Administrador;
DROP ROLE IF EXISTS Recepcionista;
DROP ROLE IF EXISTS Veterinario;
DROP ROLE IF EXISTS app; --la app en sí no hace nadota, los roles se cambian en el backend

CREATE ROLE Administrador;
GRANT ALL PRIVILEGES ON TABLE duenos TO Administrador;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO Administrador;
CREATE ROLE Recepcionista;
CREATE ROLE Veterinario;

CREATE ROLE app WITH 
LOGIN 
PASSWORD '12345678'
NOSUPERUSER
NOCREATEDB
NOCREATEROLE
NOINHERIT;

GRANT Administrador TO app;
GRANT Recepcionista TO app;
GRANT Veterinario TO app;
