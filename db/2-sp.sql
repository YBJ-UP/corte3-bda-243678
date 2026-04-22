CREATE OR REPLACE PROCEDURE sp_agendar_cita(
    p_mascota_id INT,
    p_veterinario_id INT,
    p_fecha_hora TIMESTAMP,
    p_motivo TEXT,
    OUT p_cita_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_mascota_existe BOOLEAN;
    v_vet_activo BOOLEAN;
    v_vet_descanso VARCHAR(50);
    v_dia_semana_cita VARCHAR(20);
    v_colision INT;
BEGIN
    SELECT EXISTS (SELECT 1 FROM mascotas WHERE id = p_mascota_id) INTO v_mascota_existe;
    IF NOT v_mascota_existe THEN
        RAISE EXCEPTION 'Error: La mascota con ID % no existe.', p_mascota_id;
    END IF;

    SELECT activo, dias_descanso 
    INTO v_vet_activo, v_vet_descanso
    FROM veterinarios 
    WHERE id = p_veterinario_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Error: El veterinario con ID % no existe.', p_veterinario_id;
    END IF;
    
    IF v_vet_activo IS NULL OR v_vet_activo = FALSE THEN
        RAISE EXCEPTION 'Error: El veterinario con ID % no está activo en el sistema.', p_veterinario_id;
    END IF;

    v_dia_semana_cita := trim(lower(to_char(p_fecha_hora, 'TMDay')));
    
    IF v_vet_descanso IS NOT NULL AND v_vet_descanso <> '' THEN
        IF v_dia_semana_cita = ANY(string_to_array(replace(lower(v_vet_descanso), ' ', ''), ',')) THEN
            RAISE EXCEPTION 'Error: El veterinario descansa el día %.', v_dia_semana_cita;
        END IF;
    END IF;

    SELECT id INTO v_colision
    FROM citas
    WHERE veterinario_id = p_veterinario_id 
      AND fecha_hora = p_fecha_hora;

    IF FOUND THEN
        RAISE EXCEPTION 'Error: El veterinario ya tiene una cita agendada para el horario %.', p_fecha_hora;
    END IF;

    -- 6. Insertar cita y devolver el ID
    INSERT INTO citas (mascota_id, veterinario_id, fecha_hora, motivo, estado)
    VALUES (p_mascota_id, p_veterinario_id, p_fecha_hora, p_motivo, 'AGENDADA')
    RETURNING id INTO p_cita_id;

EXCEPTION
    WHEN OTHERS THEN
        RAISE;
END;
$$;
