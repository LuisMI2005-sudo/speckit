# Contrato de interfaz: Agenda académica

## Pantalla y acciones

Una página en español con registro y catálogo de materias, formulario de tarea,
filtros por materia/estado y listado ordenado. Cada tarea muestra título, materia
por nombre y color, fecha, estado textual y alerta si corresponde. La descripción
completa debe poder consultarse, sin truncamiento irreversible.

Las materias tienen acción de borrar. Pedir confirmación con nombre de materia,
acciones «Cancelar» y «Borrar». Cancelar conserva datos y devuelve el foco a la
acción inicial. Una respuesta 409 muestra el mensaje sin quitar la materia. Tras
borrar, actualizar catálogo y selectores; si era el filtro activo, elegir «Todas las
materias» y conservar el filtro de estado. No ofrecer borrado de tareas.

Tras un guardado fallido, conservar formulario y señalar los errores; tras un éxito
confirmado, actualizar la vista y anunciarlo. Deshabilitar envíos repetidos mientras
la solicitud esté pendiente y restaurar controles al finalizar. No mostrar una
agenda vacía como sustituto de una consulta fallida: ofrecer «Reintentar».

## Longitudes y colores

Nombre 1–100, título 1–150 y descripción opcional hasta 2000 puntos de código NFC.
Contar con `Array.from`, recortar solo nombre y título; no confiar exclusivamente
en `maxlength`, que cuenta unidades UTF-16. Mostrar límite y error de campo sin
truncar el contenido. El servidor vuelve a validar todos los datos.

Paleta: azul, verde, rojo, naranja, morado y turquesa. Usar controles con nombre
accesible y selección identificable sin color. El nombre de materia siempre es visible.

## Tiempo y alertas

Función pura de JavaScript que recibe fecha_entrega, estado e instante actual.
Construir por componentes el siguiente día a las 00:00 locales, respetando calendario
local y años bajos mediante `setFullYear`; no analizar la fecha como UTC ni avanzar
sumando 86400000 ms. Usar la diferencia entre instantes para los límites:

- Completada: ninguna alerta temporal.
- Diferencia <= 0: «Vencida».
- 0 < diferencia <= 172800000 ms: «Urgente».
- Diferencia > 172800000 ms: sin alerta.

Ejemplo en America/La_Paz: entrega el 2026-10-28; límite el 2026-10-29 a las 00:00.
El 2026-10-27 a las 00:00 está exactamente a 48 horas y es urgente. El 2026-10-29
a las 00:00 está vencida. Las completadas mantienen solo su estado.

Recalcular cada 30 segundos en vista activa y al recuperar foco o visibilidad,
antes de presentar la vista recuperada. Al cambiar zona o reloj del dispositivo,
la siguiente actualización usa sus valores actuales. Los cambios de horario pueden
hacer que dos días de calendario difieran de 48 horas; la comparación es de instantes.

## Accesibilidad y adaptación

Formularios con etiquetas explícitas, errores con `aria-describedby`, foco visible,
regiones de estado para confirmaciones y resultados, y alertas textuales. Operación
completa con teclado, incluido confirmar/cancelar borrado y volver al foco previo.
Usar estructura semántica y `lang="es"`. No comunicar estado solo por color o tachado.

Diseñar primero para 360 píxeles, permitiendo apilar formularios y controles;
a 1280 píxeles aprovechar el ancho sin superposiciones ni desplazamiento horizontal.
Los textos largos deben envolver y los controles permanecer disponibles.

## Evidencia de pruebas

pytest-playwright ejecutará las cinco historias y el borrado protegido a ambos
anchos. Comprobar etiquetas, asociación de errores, foco, anuncios y controles
por rol; verificar que el ancho de contenido no supere el de la página. Probar
emoji y Unicode, reloj inyectado, límites de 48 horas ±1 ms y vencimiento ±1 ms,
fin de mes/año y una zona con cambio estacional, además de America/La_Paz.
La revisión manual complementará con lector de pantalla, teclado y legibilidad;
se registrará junto con los resultados automatizados antes de la entrega.
