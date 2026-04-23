ALTER TABLE mascotas ENABLE ROW LEVEL SECURITY;
ALTER TABLE vacunas_aplicadas ENABLE ROW LEVEL SECURITY;
ALTER TABLE citas ENABLE ROW LEVEL SECURITY;
ALTER TABLE historial_movimientos ENABLE ROW LEVEL SECURITY;
ALTER TABLE alertas ENABLE ROW LEVEL SECURITY;

-- ==========================================
-- CITAS
-- ==========================================
-- Admins y recepcionistas hacen todo con todas las citas
CREATE POLICY citas_admin_recep ON citas
    FOR ALL TO administrador, recepcionista USING (true);

-- Los veterinarios solo ven las citas de ellos 
CREATE POLICY citas_vet ON citas
    FOR ALL TO veterinario 
    USING (veterinario_id = current_setting('app.current_id')::int);

-- ==========================================
-- MASCOTAS
-- ==========================================
CREATE POLICY mascotas_admin_recep ON mascotas
    FOR ALL TO administrador, recepcionista USING (true);

-- Los veterinarios solo modifican las mascotas que ya tienen asignadas
CREATE POLICY mascotas_vet ON mascotas
    FOR ALL TO veterinario 
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
    FOR ALL TO administrador USING (true);

-- Los veterinarios solo ven las cavunas de las mascotas que ellos atienden
CREATE POLICY vacunas_vet ON vacunas_aplicadas
    FOR ALL TO veterinario 
    USING (
        mascota_id IN (
            SELECT mascota_id 
            FROM vet_atiende_mascota 
            WHERE vet_id = current_setting('app.current_id')::int
        )
    );


-- Historial de movimientos

CREATE POLICY admin_only ON historial_movimientos
	FOR ALL TO administrador USING (true);

-- alertas

CREATE POLICY admin_only ON alertas
	FOR ALL TO administrador USING (true);
