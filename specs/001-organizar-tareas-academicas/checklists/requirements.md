# Lista de verificación de calidad: Organizador de tareas académicas de la UPB

**Propósito**: Validar que la especificación sea completa, clara y apta para planificación.
**Creación**: 2026-10-26
**Funcionalidad**: [Especificación del organizador](../spec.md)
**Resultado**: Revisión documental satisfactoria; 20 de 20 controles completos.

## Calidad del contenido

- [x] CHK001 Los comportamientos no imponen diseño; la pila expresamente solicitada se registra como restricción.
- [x] CHK002 El contenido se centra en el valor para el estudiante y la organización académica.
- [x] CHK003 La redacción es comprensible para participantes no técnicos.
- [x] CHK004 Todas las secciones obligatorias de la plantilla están completas.
- [x] CHK005 Todo el contenido está en español, salvo identificadores y rutas técnicas.

## Integridad de los requisitos

- [x] CHK006 No quedan decisiones esenciales pendientes ni marcadores de aclaración.
- [x] CHK007 Los requisitos son verificables y no ambiguos: estados, filtros y reglas temporales explícitos.
- [x] CHK008 Los criterios de éxito contienen cantidades, porcentajes o tiempos verificables.
- [x] CHK009 Los criterios de éxito no dependen de una tecnología concreta.
- [x] CHK010 Las cinco historias tienen escenarios de aceptación con condiciones y resultados observables.
- [x] CHK011 Se describen casos límite de validación, fechas, empates, fallos y persistencia.
- [x] CHK012 El alcance distingue las funciones incluidas de las excluidas de esta primera versión.
- [x] CHK013 Se documentan supuestos, dependencias, agenda por instalación y condiciones de verificación independiente.

## Preparación de la funcionalidad

- [x] CHK014 Los requisitos funcionales se vinculan con escenarios de aceptación o controles de entrega.
- [x] CHK015 Los escenarios cubren registrar y borrar materias vacías, crear y consultar tareas, completar y filtrar.
- [x] CHK016 Los resultados medibles SC-001 a SC-009 permiten evaluar los objetivos especificados.
- [x] CHK017 La especificación describe comportamientos y restricciones; el diseño técnico queda en el plan.

## Coherencia con la constitución

- [x] CHK018 Se acota una solución mínima y se exigen pruebas automatizadas antes de finalizar cada funcionalidad.
- [x] CHK019 Cada dato del usuario tiene reglas de validación y casos válidos, inválidos y límite pertinentes.
- [x] CHK020 Se exigen flujos a 360 y 1280 píxeles, teclado, foco, etiquetas y comunicación sin depender del color.

## Notas

- Revisión actualizada el 2026-10-26 tras tres preguntas respondidas y la planificación.
- Borrado confirmado: solo materias sin tareas, con confirmación; pendientes y
  completadas bloquean por igual. Se añadieron FR-017 y SC-009.
- Límites confirmados: 100/150/2000, normalización NFC, recorte de nombre/título,
  conteo por puntos de código y rechazo de excesos sin truncamiento.
- Urgencia confirmada: pendiente con 0 < tiempo restante <= 48 horas hasta la
  medianoche local del día siguiente; al alcanzar ese límite está vencida.
- La pila solicitada se documenta como restricción. SQLite cambia el supuesto de
  persistencia a una agenda por instalación, compartida por perfiles de navegador.
- No quedan contradicciones de alcance: se permite borrar materias vacías, pero
  no tareas. No hay aclaraciones obligatorias pendientes.
- Cobertura de aclaración: alcance, dominio, interacción, casos límite, restricciones,
  terminología y finalización resueltos; calidad, dependencias y estructura técnica
  detalladas en plan.md, research.md, data-model.md, contratos y quickstart.md.
- Esta revisión documental no afirma que exista implementación ni pruebas ejecutadas.
- Siguiente fase habilitada: `/speckit-tasks`.

## Cobertura de la aclaración y planificación

Tres preguntas formuladas y respondidas; ninguna respuesta pendiente.

| Categoría revisada | Estado | Evidencia |
|--------------------|--------|-----------|
| Alcance y comportamiento | Resuelto | Borrado acotado en FR-017 y exclusiones |
| Dominio y datos | Resuelto | Restricción de borrado y data-model.md |
| Interacción y experiencia | Resuelto | Confirmación, cancelación y filtros en contracts/interfaz.md |
| Atributos de calidad | Claro | SC-001 a SC-009 y estrategia de pruebas del plan |
| Integraciones y dependencias | Resuelto | Pila solicitada y decisiones de research.md |
| Casos límite y fallos | Resuelto | Longitudes, fronteras temporales, rollback y conflictos |
| Restricciones y alternativas | Resuelto | Un proyecto local; sin Docker ni microservicios |
| Terminología y consistencia | Claro | Estados y alertas separados; agenda por instalación |
| Señales de finalización | Claro | Pruebas obligatorias y criterios medibles |
| Marcadores y ambigüedades | Resuelto | Sin decisiones esenciales pendientes |
