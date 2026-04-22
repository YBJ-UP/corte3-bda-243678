ALTER TABLE mascotas ENABLE ROW LEVEL SECURITY;
ALTER TABLE vacunas_aplicadas ENABLE ROW LEVEL SECURITY;
ALTER TABLE citas ENABLE ROW LEVEL SECURITY;

-- ==========================================
-- CITAS
-- ==========================================
-- Admins y recepcionistas hacen todo con todas las citas
CREATE POLICY citas_admin_recep ON citas
    FOR ALL TO Administrador, Recepcionista USING (true);

-- Los veterinarios solo ven las citas de ellos 
CREATE POLICY citas_vet ON citas
    FOR ALL TO Veterinario 
    USING (veterinario_id = current_setting('app.current_id')::int);

-- ==========================================
-- MASCOTAS
-- ==========================================
CREATE POLICY mascotas_admin_recep ON mascotas
    FOR ALL TO Administrador, Recepcionista USING (true);

-- Los veterinarios solo modifican las mascotas que ya tienen asignadas
CREATE POLICY mascotas_vet ON mascotas
    FOR ALL TO Veterinario 
    USING (
        id IN (
            SELECT mascota_id 
            FROM vet_atiende_mascota 
            WHERE vet_id = current_setting('app.current_id')::int
        )
    );

-- ==========================================
-- VACUNAS_APLICADAS
-- ==========================================
CREATE POLICY vacunas_admin ON vacunas_aplicadas
    FOR ALL TO Administrador USING (true);

-- Los veterinarios solo ven las cavunas de las mascotas que ellos atienden
CREATE POLICY vacunas_vet ON vacunas_aplicadas
    FOR ALL TO Veterinario 
    USING (
        mascota_id IN (
            SELECT mascota_id 
            FROM vet_atiende_mascota 
            WHERE vet_id = current_setting('app.current_id')::int
        )
    );
