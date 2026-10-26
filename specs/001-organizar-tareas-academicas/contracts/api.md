# Contrato de API: Agenda académica

**Formato**: JSON con claves y mensajes en español, UTF-8. Mismo origen que la interfaz.
**Ámbito**: Una agenda por instancia local, sin autenticación ni parámetro de usuario.
Las entradas no admiten campos desconocidos. Las reglas de spec.md son obligatorias.

## Recursos y operaciones

| Método | Ruta | Entrada | Éxito | Errores previstos |
|--------|------|---------|-------|-------------------|
| GET | / | Sin cuerpo | 200 HTML de la aplicación | 500 |
| GET | /static/{archivo} | Archivo del directorio estático | 200 recurso | 404 |
| GET | /api/materias | Sin cuerpo | 200 lista de materias por id | 503 |
| POST | /api/materias | nombre, color | 201 materia creada | 409 duplicada, 422, 503 |
| DELETE | /api/materias/{id} | id entero positivo | 204 sin cuerpo | 404, 409 con tareas, 422, 503 |
| GET | /api/tareas | Filtros opcionales materia_id y estado | 200 lista ordenada | 422, 503 |
| POST | /api/tareas | materia_id, titulo, descripcion opcional, fecha_entrega | 201 tarea pendiente | 422, 503 |
| PATCH | /api/tareas/{id}/completar | Sin cuerpo | 200 tarea completada | 404, 422, 503 |

Los filtros ausentes significan todas las materias y todos los estados. `estado`
solo admite `pendiente` o `completada`; no enviar la etiqueta «Todas». Una materia
filtrada inexistente se rechaza con 422, no se confunde con cero coincidencias.
El orden de tareas es siempre fecha_entrega ascendente y después id ascendente.

## Esquemas y ejemplos

Crear materia:

```json
{"nombre":"Cálculo I","color":"azul"}
```

Materia devuelta:

```json
{"id":1,"nombre":"Cálculo I","color":"azul"}
```

Crear tarea; `descripcion` omitida o nula se normaliza a cadena vacía:

```json
{"materia_id":1,"titulo":"Resolver práctica 1","descripcion":"Ejercicios 1 a 5","fecha_entrega":"2026-10-28"}
```

Tarea devuelta por alta, listado o completado:

```json
{"id":1,"materia_id":1,"titulo":"Resolver práctica 1","descripcion":"Ejercicios 1 a 5","fecha_entrega":"2026-10-28","estado":"pendiente"}
```

Los listados son arreglos JSON; sin coincidencias devuelven `[]`. La interfaz
resuelve nombre y color de materia desde el catálogo. No se devuelve una alerta
calculada con la hora del servidor. El completado devuelve el mismo esquema con
`estado: "completada"`; repetir la petición conserva el registro e identidad.

## Validación

- `nombre`: texto NFC recortado, 1–100 puntos de código, clave única por casefold.
- `titulo`: texto NFC recortado, 1–150 puntos de código.
- `descripcion`: texto NFC opcional, hasta 2000 puntos de código.
- `color`: azul, verde, rojo, naranja, morado o turquesa.
- `materia_id` e identificadores de ruta: enteros positivos, no booleanos ni fracciones.
- `fecha_entrega`: cadena exacta AAAA-MM-DD que representa una fecha real;
  no aceptar fecha con hora, número de época ni conversión automática ambigua.
- Validar existencia de materia antes del alta y garantizarla también mediante FK.
- Nombre, título y descripción rechazan NUL; entradas excesivas nunca se truncan.

## Errores

Formato estable para todos los fallos, incluidos JSON mal formado y validación:

```json
{"error":{"codigo":"validacion","mensaje":"Revisa los datos ingresados","campos":{"titulo":"Ingresa un título de 1 a 150 caracteres"}}}
```

| Estado | Código | Mensaje representativo |
|--------|--------|------------------------|
| 404 | no_encontrado | La materia no existe / La tarea no existe |
| 409 | materia_duplicada | Esta materia ya existe |
| 409 | materia_con_tareas | No puedes borrar una materia con tareas |
| 422 | validacion | Revisa los datos ingresados |
| 503 | almacenamiento_no_disponible | No se pudieron guardar o recuperar los datos. Intenta de nuevo |
| 500 | error_interno | Ocurrió un error inesperado |

`campos` es un objeto vacío para errores no asociados a un campo. No exponer SQL,
rutas internas ni trazas. La API no informa éxito antes del commit. Si una carrera
elimina la materia antes del alta de tarea, devolver 422 asociado a materia_id.
Un bloqueo temporal devuelve 503 y revierte cualquier cambio no confirmado.

## Comprobaciones del contrato

Pruebas con pytest/TestClient para cada operación y error, duplicado Unicode,
límites exactos, filtros por intersección, completado idempotente, persistencia y
borrado restringido para tareas pendientes/completadas. La confirmación de borrado
es una interacción de interfaz, no una contraseña o permiso de API.
