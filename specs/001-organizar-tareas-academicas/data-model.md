# Modelo de datos: Agenda académica

**Fecha**: 2026-10-26
**Persistencia**: Un archivo SQLite por instalación; no existen usuarios ni sesiones.

## Materia

| Campo | Tipo | Restricciones |
|-------|------|---------------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | Identidad positiva, no reutilizada |
| nombre | TEXT NOT NULL | NFC, espacios exteriores recortados, 1–100 puntos de código |
| nombre_clave | TEXT NOT NULL UNIQUE | `casefold()` del nombre normalizado; generado solo por servidor |
| color | TEXT NOT NULL | Uno de azul, verde, rojo, naranja, morado, turquesa |

La clave de nombre mantiene diferencias de tildes, pero no de mayúsculas. Los
colores son códigos de dominio estables; el CSS fija sus valores visuales. Dos
materias pueden compartir color. Aplicar `CHECK(length(nombre) BETWEEN 1 AND 100)`
y `CHECK(color IN (...))` además de validación del servidor.

## Tarea

| Campo | Tipo | Restricciones |
|-------|------|---------------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | Identidad y desempate por creación |
| materia_id | INTEGER NOT NULL | Referencia a materias(id), ON DELETE RESTRICT |
| titulo | TEXT NOT NULL | NFC y recorte exterior, 1–150 puntos de código |
| descripcion | TEXT NOT NULL DEFAULT '' | NFC, 0–2000 puntos de código; solo espacios equivale a vacío |
| fecha_entrega | TEXT NOT NULL | Fecha válida de calendario en formato AAAA-MM-DD |
| estado | TEXT NOT NULL DEFAULT 'pendiente' | pendiente o completada |

Aplicar CHECK a longitudes y estado. Validar la fecha con el tipo de fecha del
servidor y serializar sin hora. No usar conversores automáticos de fecha de SQLite.
No se exige unicidad de título ni de combinación materia/fecha.

Consultar con `ORDER BY fecha_entrega ASC, id ASC`. No se necesita fecha de creación
adicional para el desempate. Un índice en `tareas(materia_id)` sirve al filtro y a
la integridad referencial. Con cien tareas no se necesitan otros índices iniciales.

## Relaciones e invariantes

- Una materia tiene cero o más tareas; cada tarea tiene exactamente una materia.
- Borrar una materia sin tareas requiere confirmación en la interfaz y elimina
  únicamente esa materia; el servidor comprueba de nuevo la integridad al borrar.
- Si existe cualquier tarea, incluso completada, SQLite impide el borrado; la API
  devuelve 409 sin alterar datos. No se implementa cascada, reasignación ni orfandad.
- Ante una carrera entre crear tarea y borrar materia, la restricción garantiza
  que no se confirmen ambas operaciones dejando una referencia inválida.
- Borrar una materia inexistente devuelve 404. Cancelar no envía petición de borrado.
- Confirmar transacciones antes de responder éxito; revertir ante excepciones.

## Ciclos de vida

**Materia**: inexistente → registrada → borrada únicamente si está vacía.
**Tarea**: inexistente → pendiente → completada. Repetir completado no cambia datos.
No hay transición inversa ni borrado de tareas en esta versión.

**Alerta derivada**, calculada en el navegador, nunca persistida:

1. Si estado es completada: sin alerta.
2. Construir el inicio local del día siguiente a fecha_entrega.
3. Restar el instante actual; resultado menor o igual a cero: vencida.
4. Resultado mayor a cero y menor o igual a 172800000 ms: urgente.
5. Resultado mayor a 172800000 ms: sin alerta.

La fecha guardada permanece igual al cambiar la zona horaria. La medianoche y las
48 horas se vuelven a calcular según la zona y reloj actuales del dispositivo.

## Normalización y validación

Normalizar NFC antes del conteo. Python cuenta puntos de código con `len`, y JS
con `Array.from`. Rechazar caracteres NUL para evitar diferencias de longitud con
SQLite; rechazar datos de tipos incorrectos y campos desconocidos de entrada.
La descripción se conserva cuando no es completamente blanca; no recortarla ni
truncarla silenciosamente. El servidor determina unicidad y existencia de materia.

## Inicialización y recuperación

Crear el esquema si no existe al iniciar; no borrar ni recrear tablas existentes.
No generar datos de demostración en la agenda real. Una ruta alternativa de datos
permite pruebas y futuras instalaciones sin cambiar código. Ignorar `data/` en Git.
Los errores de lectura se informan como tales; no crear una agenda vacía como
sustitución silenciosa de un archivo inaccesible o corrupto. Evoluciones del esquema
quedan fuera de esta primera creación y exigirán un cambio documentado posterior.
