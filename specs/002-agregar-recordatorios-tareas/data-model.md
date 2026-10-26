# Modelo de datos

Materias y tareas siguen el modelo de 001: nombres NFC recortados 1–100, clave por
casefold única, color de paleta; título 1–150, descripción 0–2000, fecha sin hora,
estado pendiente/completada. Borrado de materia restringido por FK, incluso completadas.

## Recordatorio

- Clave primaria compuesta: tarea_id y fecha_entrega.
- resultado: no_emitido, incierto o emitido.
- token: identificador aleatorio único para la reserva actual.
- autorizado: 0/1 para impedir autorizaciones duplicadas de un mismo token.
- Relación: tarea existente obligatoria. Sin datos de contacto ni usuarios.

Transiciones: ausencia/no_emitido → incierto al reservar; incierto → emitido
si el navegador acepta; incierto → no_emitido ante fracaso inequívoco. Cierre o
respuesta perdida conserva incierto. Emitido es terminal. Resultados repetidos
iguales con el mismo token se aceptan sin cambios; resultados contradictorios se rechazan.

Cada escritura abre BEGIN IMMEDIATE y confirma o revierte; PRAGMA foreign_keys=ON
en cada conexión. Reserva y autorización comprueban estado y fecha actuales.
El reloj y zona se validan, no se guardan como preferencias globales del usuario.
