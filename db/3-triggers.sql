CREATE OR REPLACE FUNCTION fn_trg_historial_cita()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_mascota_nombre VARCHAR(50);
    v_vet_nombre VARCHAR(100);
    v_descripcion TEXT;
BEGIN
    SELECT nombre INTO v_mascota_nombre FROM mascotas WHERE id = NEW.mascota_id;
    SELECT nombre INTO v_vet_nombre FROM veterinarios WHERE id = NEW.veterinario_id;

    v_descripcion := format('Cita para %s con %s el %s', 
                            v_mascota_nombre, 
                            v_vet_nombre, 
                            to_char(NEW.fecha_hora, 'DD/MM/YYYY HH24:MI'));

    INSERT INTO historial_movimientos (tipo, referencia_id, descripcion)
    VALUES ('CITA_AGENDADA', NEW.id, v_descripcion);

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_historial_cita
AFTER INSERT ON citas
FOR EACH ROW
EXECUTE FUNCTION fn_trg_historial_cita();
