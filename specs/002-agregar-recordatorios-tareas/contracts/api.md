# Contratos de la agenda y recordatorios

JSON y errores en español. Entradas estrictas; rechazar campos desconocidos.
Formato de error: {"error":{"codigo":"validacion","mensaje":"Revisa los datos ingresados","campos":{}}}.
422 validación, 404 inexistente, 409 conflicto y 503 almacenamiento no disponible.

## Agenda base

GET/POST /api/materias: arreglo o alta con {nombre,color}; DELETE /api/materias/{id}
solo vacías, 204, 409 con tareas. Paleta: azul, verde, rojo, naranja, morado, turquesa.
GET/POST /api/tareas: filtros opcionales materia_id/estado y alta con
{materia_id,titulo,descripcion opcional,fecha_entrega}. Orden fecha_entrega/id.
PATCH /api/tareas/{id}/completar: sin cuerpo, idempotente; no reapertura.

## Recordatorios

Contexto = {ahora: instante ISO con zona, zona: nombre IANA válido del dispositivo}.

- POST /api/recordatorios/reservar con Contexto: 200 arreglo de reservas ganadas
  {token,tarea_id,titulo,materia,fecha_entrega}; solo pendientes para mañana desde
  las 09:00 locales, sin reservas previas inciertas/emitidas.
- POST /api/recordatorios/{token}/autorizar con Contexto: 200 datos actuales de tarea
  y materia; una sola autorización, solo con ventana y estado válidos; 409 si no.
- POST /api/recordatorios/{token}/resultado con {resultado: emitido|no_emitido}:
  200 confirmación; token debe existir y estar autorizado; igual confirmación es
  idempotente, contradicción 409. Permiso no se acepta como autorización del servidor.
- GET /api/recordatorios: arreglo de estados persistidos sin exponer tokens;
  permite informar resultados inciertos al recuperar la agenda.

Los resultados fallidos de escritura no afirman éxito. No reenviar al perder una
respuesta de reserva/autorización. Los tokens no permiten modificar tarea/fecha.

## Interfaz

Activar recordatorios con gesto explícito y mostrar disponibilidad en texto.
Evaluar cada 30 segundos, al abrir, recuperar foco/visibilidad, conceder permiso y
guardar/completar. Registrar /sw.js con alcance /; showNotification incluye título,
materia y fecha, no descripción. Sin tareas de fondo con página cerrada.

Mantener los formularios base, errores asociados, avisos aria-live, teclado,
foco visible y anchos 360/1280. Tras borrar, enfocar encabezado del catálogo; al
cancelar, devolver foco al botón inicial. En fallo incierto de alta no reintentar
sin consultar el listado; no se añade idempotencia general ajena a esta extensión.
