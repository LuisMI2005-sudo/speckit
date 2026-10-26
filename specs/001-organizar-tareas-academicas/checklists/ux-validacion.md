# Lista de verificación: Experiencia de usuario y validación de datos

**Propósito**: Revisar la integridad, claridad, coherencia y cobertura de los requisitos del organizador académico de la UPB.
**Creación**: 2026-10-26
**Funcionalidad**: [Especificación](../spec.md)
**Profundidad**: Estándar, con énfasis en pérdida de datos, límites y comprensión de alertas.
**Destinatarios y momento**: Autor y revisor de requisitos, antes del desglose en tareas y la implementación.
**Estado**: Pendiente de revisión; los controles se entregan sin marcar.

**Referencias**: «Especificación» corresponde a [spec.md](../spec.md);
«Plan» a [plan.md](../plan.md); «Modelo de datos» a [data-model.md](../data-model.md);
los contratos de [interfaz](../contracts/interfaz.md) y [API](../contracts/api.md)
completan los requisitos. Todavía no existe tasks.md.

Los controles evalúan lo escrito en estos documentos. Las etiquetas «Carencia»
señalan puntos cuya cobertura debe revisarse, sin dar por aprobada una solución
ni ampliar automáticamente el alcance acordado.

## Integridad de los requisitos de experiencia de usuario

- [ ] CHK001 ¿Se especifican los datos y acciones disponibles en cada flujo principal: materias, tareas, consulta, completado y filtros? [Integridad; Especificación §Historias 1–5; FR-002 a FR-010]
- [ ] CHK002 ¿Se distingue explícitamente entre una agenda sin tareas, la ausencia de materias y un filtro sin coincidencias, con una acción de continuación para cada caso? [Cobertura; Especificación §Historias 2.4, 3.7 y 5.4; FR-011]
- [ ] CHK003 ¿Están definidos los estados de espera, la prevención de envíos repetidos y la restitución de los controles tras éxito o error para cada operación que modifica datos? [Integridad; Contrato de interfaz §Pantalla y acciones]
- [ ] CHK004 ¿Se documenta cómo consultar la descripción completa y cómo se presentan textos largos sin perder información ni ocultar acciones? [Claridad; Especificación §FR-005; Contrato de interfaz §Pantalla y acciones y §Accesibilidad y adaptación]

## Claridad del listado, los estados y los filtros

- [ ] CHK005 ¿Se especifican el orden ascendente por fecha y el criterio de desempate de forma idéntica para el listado completo y los resultados filtrados? [Consistencia; Especificación §FR-006, FR-009 y §Casos límite]
- [ ] CHK006 ¿Se distinguen sin ambigüedad los estados «Pendiente» y «Completada» de las alertas «Urgente» y «Vencida», sin exigir un filtro adicional de alertas? [Claridad; Especificación §FR-007 a FR-009]
- [ ] CHK007 ¿Se define la combinación por intersección de materia y estado, los valores iniciales y el resultado de restablecer filtros? [Integridad; Especificación §FR-009, FR-010 y §Historia 5]
- [ ] CHK008 ¿Se describe qué ocurre al completar una tarea bajo el filtro «Pendientes», incluida su desaparición y el aviso de confirmación? [Cobertura; Especificación §Historia 4.3; UI-003]

## Borrado de materias y protección de datos

- [ ] CHK009 ¿Está expresamente indicado que cualquier tarea asociada, pendiente o completada, impide borrar su materia, sin cascada ni tareas huérfanas? [Claridad; Especificación §FR-017 y §Historia 1.6]
- [ ] CHK010 ¿Se documentan la identificación de la materia en la confirmación, las opciones de confirmar o cancelar y la ausencia de cambios al cancelar? [Integridad; Especificación §Historia 1.5–1.7; Contrato de interfaz §Pantalla y acciones]
- [ ] CHK011 ¿Se especifican la actualización de selectores y el restablecimiento del filtro de materia, conservando el estado seleccionado, después de borrar una materia vacía? [Consistencia; Especificación §FR-017 y §Casos límite]
- [ ] CHK012 ¿Se define un destino de foco válido tras un borrado satisfactorio cuando el control que lo inició ya no existe? [Carencia; Contrato de interfaz §Pantalla y acciones y §Accesibilidad y adaptación]

## Integridad y claridad de la validación de campos

- [ ] CHK013 ¿La obligatoriedad del nombre, color, materia, título y fecha está diferenciada de la descripción opcional para todos los formularios? [Integridad; Especificación §FR-002, FR-004 y §Validación de entradas]
- [ ] CHK014 ¿Se establecen explícitamente los límites inclusivos de 1–100 para materia, 1–150 para título y 0–2000 para descripción, con rechazo de excesos sin truncamiento? [Claridad; Especificación §Aclaraciones y §Validación de entradas]
- [ ] CHK015 ¿Se define el orden de normalización y recorte previo al conteo, su aplicación por campo y el significado de «carácter» para tildes, emoji y secuencias compuestas? [Claridad; Especificación §Validación de entradas; Modelo de datos §Normalización y validación]
- [ ] CHK016 ¿Se documenta de forma consistente la diferencia entre descripción ausente, nula, vacía o formada solo por espacios y una descripción con contenido significativo? [Consistencia; Especificación §Validación de entradas; Contrato de API §Esquemas y ejemplos]

## Cobertura de valores inválidos y relaciones

- [ ] CHK017 ¿Se precisa cómo detectar nombres de materia duplicados ante diferencias de mayúsculas, espacios exteriores y tildes, sin impedir títulos de tarea repetidos? [Claridad; Especificación §FR-003 y §Casos límite; Modelo de datos §Materia y §Tarea]
- [ ] CHK018 ¿Se especifican los valores de color permitidos, su selección obligatoria y la posibilidad de compartir color entre materias? [Integridad; Especificación §Validación de entradas y §Supuestos y alcance mínimo; Contrato de interfaz §Longitudes y colores]
- [ ] CHK019 ¿Se exige que la materia asociada exista y se define el rechazo de referencias inválidas, incluida su eliminación concurrente durante el registro de una tarea? [Cobertura; Especificación §FR-004 y §Casos límite; Contrato de API §Errores]
- [ ] CHK020 ¿Se documentan fechas imposibles, años bisiestos, tipos incorrectos, campos desconocidos y caracteres no admitidos, conservando la admisión de fechas pasadas? [Cobertura; Especificación §Validación de entradas y §Casos límite; Modelo de datos §Normalización y validación; Contrato de API §Validación]

## Precisión de vencimientos y urgencia

- [ ] CHK021 ¿Se define la fecha de entrega como un día de calendario cuyo límite es el inicio del día siguiente a las 00:00 en la zona local del dispositivo? [Claridad; Especificación §Reglas de fecha, vencimiento y urgencia]
- [ ] CHK022 ¿Quedan especificados los tres intervalos de pendientes: tiempo restante menor o igual a cero, mayor a cero y hasta 48 horas inclusive, y mayor a 48 horas? [Medición; Especificación §FR-007 y §Reglas de fecha, vencimiento y urgencia]
- [ ] CHK023 ¿Los requisitos excluyen a las tareas completadas de toda alerta temporal y contemplan cambios de día, zona horaria y horario estacional sin cambiar la fecha guardada? [Consistencia; Especificación §Historia 3.5 y §Reglas de fecha, vencimiento y urgencia; Contrato de interfaz §Tiempo y alertas]
- [ ] CHK024 ¿Se cuantifican la actualización de alertas en una vista activa y el recálculo al volver a ella, de manera coherente entre especificación y contrato de interfaz? [Medición; Especificación §FR-015; Contrato de interfaz §Tiempo y alertas]

## Errores, recuperación y consistencia de las respuestas

- [ ] CHK025 ¿Se exigen mensajes en español asociados a cada campo inválido, conservación de los datos ingresados y validación antes de procesar o guardar en todos los puntos de entrada? [Integridad; Especificación §FR-013, FR-014, UI-003 y §Validación de entradas]
- [ ] CHK026 ¿Se distingue un fallo de recuperación de una agenda vacía y se define el reintento sin sobrescribir datos ni comunicar un éxito inexistente? [Cobertura; Especificación §Casos límite; Contrato de interfaz §Pantalla y acciones]
- [ ] CHK027 ¿Están definidos el resultado visible y la conservación íntegra de datos ante un fallo de guardado, borrado rechazado o conflicto concurrente? [Cobertura; Especificación §FR-013, FR-017 y §Casos límite; Contrato de API §Errores]
- [ ] CHK028 ¿Se especifica cómo comunicar una operación que exceda el tiempo de espera y cómo evitar duplicados al reintentar cuando su resultado anterior sea incierto? [Carencia; Especificación §FR-013 y §Casos límite; Contrato de interfaz §Pantalla y acciones]

## Accesibilidad, medición y supuestos de uso

- [ ] CHK029 ¿Los requisitos de 360 y 1280 píxeles incluyen todos los flujos, confirmación de borrado y mensajes de validación, con criterios objetivos de pérdida de contenido, superposición y desplazamiento horizontal? [Consistencia; Especificación §UI-001, SC-006; Contrato de interfaz §Accesibilidad y adaptación]
- [ ] CHK030 ¿Se especifican teclado, foco visible, etiquetas, errores asociados, anuncios de resultados y reconocimiento de materia, alerta y estado sin depender solo del color? [Integridad; Especificación §UI-002 a UI-004; Contrato de interfaz §Accesibilidad y adaptación]
- [ ] CHK031 ¿Los criterios de aceptación cubren límites y errores de campos, fronteras temporales y borrado protegido, con resultados medibles y pruebas automatizadas obligatorias? [Trazabilidad; Especificación §FR-016, SC-003, SC-005, SC-007 y SC-009; Plan §Estrategia de pruebas y entrega]
- [ ] CHK032 ¿Se documentan las expectativas de conservación y uso compartido de la agenda por instalación, sin sugerir que otro perfil de navegador crea un usuario independiente? [Supuesto; Especificación §FR-001, FR-012 y §Supuestos y alcance mínimo]
## Notas de revisión

- Marcar `[x]` únicamente cuando el requisito esté documentado con suficiente claridad y referencia.
- Registrar hallazgos junto al control, indicando el documento, sección y decisión necesaria.
- Una respuesta negativa identifica una carencia documental; no implica por sí sola un defecto de código.
- Los controles sobre carencias no sustituyen una aclaración acordada ni autorizan cambios de alcance.
- Esta lista complementa requirements.md y no sustituye las pruebas automatizadas obligatorias.
