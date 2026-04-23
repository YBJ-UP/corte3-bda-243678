-- 3 ROLES - VETERINARIO, RECEPCION Y ADMINISTRADORES

-- Veterinario
-- Solo ve las mascotas que él atiende (según vet_atiende_mascota). Puede registrar nuevas citas y
-- aplicar vacunas a sus mascotas. No puede ver historial médico de mascotas que no atiende.

-- Recepción
-- Ve todas las mascotas y sus dueños (datos de contacto). Puede agendar citas para cualquier mascota.
-- No puede ver vacunas aplicadas (información médica).

-- Administrador
-- Ve todo. Puede crear usuarios, asignar mascotas a veterinarios, y gestionar inventario de vacunas.

DROP ROLE IF EXISTS administrador;
DROP ROLE IF EXISTS recepcionista;
DROP ROLE IF EXISTS veterinario;
DROP ROLE IF EXISTS app; --la app en sí no hace nadota, los roles se cambian en el backend

CREATE ROLE administrador;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO administrador;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO administrador;

CREATE ROLE recepcionista;
GRANT SELECT, INSERT, UPDATE, DELETE ON duenos, mascotas, citas TO recepcionista;
GRANT SELECT ON veterinarios TO recepcionista;
REVOKE ALL PRIVILEGES ON vacunas_aplicadas, inventario_vacunas, historial_movimientos, alertas FROM recepcionista;

CREATE ROLE veterinario;
GRANT SELECT, INSERT, UPDATE ON mascotas, citas, vacunas_aplicadas TO veterinario;
GRANT SELECT ON inventario_vacunas, duenos, veterinarios TO veterinario;
REVOKE ALL PRIVILEGES ON historial_movimientos, alertas FROM veterinario;

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
