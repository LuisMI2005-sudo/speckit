# Tareas: Organizador de tareas académicas de la UPB

**Fecha**: 2026-10-26
**Entrada**: spec.md, plan.md, research.md, data-model.md, contracts/api.md,
contracts/interfaz.md y quickstart.md de esta funcionalidad.
**Rama**: `001-organizar-tareas-academicas`
**Estado**: Pendiente de implementación; ninguna tarea ejecutada.
**Pruebas**: Obligatorias para toda funcionalidad, incluidos límites y errores.
**Idioma**: Código documentado, mensajes y documentos en español; conservar nombres técnicos necesarios.
**Trabajo en equipo**: Consultar el [plan de trabajo para dos integrantes](../plan-trabajo-equipo.md) para responsables, archivos exclusivos y orden de integración.

## Formato y rutas

Cada tarea usa casilla, identificador consecutivo, etiqueta de historia cuando
corresponde y rutas relativas a la raíz del proyecto. `[P]` permite trabajo paralelo
solo dentro de los grupos independientes indicados al final. Las funciones nuevas
deben tener nombres claros, responsabilidades pequeñas y comentarios de lo no obvio.
No añadir capas, servicios, dependencias ni funcionalidades ajenas al plan.

Los registros de ejecución se crearán en
`specs/001-organizar-tareas-academicas/evidencias.md`; es documentación de entrega,
no una nueva capa del producto. Cada verificación debe añadir comando, resultado,
fecha y escenarios cubiertos, sin afirmar éxito si las pruebas todavía fallan.

## Fase 1: Preparación

- [ ] T001 Preparar el paquete mínimo en app/__init__.py y fijar dependencias compatibles con Python 3.12 en requirements.txt y requirements-dev.txt: FastAPI/Uvicorn y pytest/httpx/pytest-playwright, sin ORM ni compilación de frontend (plan §Contexto técnico).
- [ ] T002 [P] Configurar descubrimiento de pruebas en pytest.ini y documentar instalación de Chromium y comandos reproducibles en specs/001-organizar-tareas-academicas/quickstart.md (FR-016).
- [ ] T003 [P] Excluir entorno virtual, cachés y data/agenda.sqlite3 mediante .gitignore, conservando el archivo SQLite fuera de los recursos públicos (FR-012).
- [ ] T004 Revisar los 32 controles de specs/001-organizar-tareas-academicas/checklists/ux-validacion.md y registrar carencias y decisiones necesarias en specs/001-organizar-tareas-academicas/evidencias.md, sin marcarlas resueltas sin evidencia ni cambiar el alcance automáticamente (UI-001 a UI-005).

## Fase 2: Fundamentos compartidos

**Bloqueo**: Finalizar esta fase antes de las historias. No se implementan cuentas,
contenedores, microservicios ni una agenda duplicada en el navegador.

- [ ] T005 Crear en app/db.py el esquema de materias y tareas de data-model.md con claves no reutilizadas, nombre_clave UNIQUE, límites CHECK, estados permitidos, índice materia_id y referencia ON DELETE RESTRICT; inicializar sin borrar datos (FR-002, FR-004, FR-012, FR-017).
- [ ] T006 Gestionar en app/db.py conexiones por operación, UPB_DB_PATH, claves foráneas activadas antes de transacciones, parámetros SQL, commit/rollback y cierre garantizado; distinguir archivo inaccesible de agenda nueva y traducir bloqueos sin guardar parcialmente (FR-012, FR-013, FR-014).
- [ ] T007 Implementar en app/main.py crear_app(ruta_db), ciclo de vida, exportación app, respuesta de / y montaje exclusivo de app/static/; normalizar errores al contrato JSON en español sin trazas ni datos internos (FR-001, FR-014).
- [ ] T008 Crear en tests/conftest.py SQLite temporal por prueba, cliente de API, servidor efímero de navegador con limpieza y datos preparados de materias/tareas sin dependencia de otras historias; parametrizar anchos 360/1280 (FR-016; UI-005).
- [ ] T009 Crear en tests/test_persistencia.py pruebas de esquema, claves foráneas por conexión, rollback ante fallo, archivo inaccesible y reapertura de una segunda app contra el mismo archivo; comprobar que /static/ no exponga datos (FR-012, FR-013, FR-014).
- [ ] T010 Preparar app/static/index.html, app/static/styles.css y app/static/app.js con estructura semántica en español, regiones de avisos, funciones de petición JSON, estados de espera y manejo de errores sin pérdida del formulario; probar /, estáticos y errores generales en tests/test_api.py (FR-014; UI-001 a UI-003).

**Punto de control**: Ejecutar las pruebas compartidas y registrar el resultado en
evidencias.md antes de dar por terminada la fase. El archivo de datos real no se usa en pruebas.

## Fase 3: Historia 1 — Registrar y borrar materias vacías (P1)

**Objetivo**: Catálogo persistente con nombre/color y borrado protegido.
**Prueba independiente**: Crear una materia, reabrir su agenda y borrar una vacía;
con tareas preparadas, rechazar el borrado sin alterar registros.

### Pruebas automatizadas obligatorias

- [ ] T011 [P] [US1] Añadir en tests/test_reglas.py casos de nombre vacío/espacios, 1/100/101 puntos de código, NFC, emoji, tildes, NUL, recorte y duplicados por mayúsculas sin confundir tildes (FR-003, FR-013; SC-005).
- [ ] T012 [P] [US1] Añadir en tests/test_api.py casos de GET/POST/DELETE de materias, paleta válida/inválida, 404, 409 duplicado, 422, bloqueo con tareas pendientes/completadas y carrera crear tarea/borrar materia sin huérfanas; preparar datos directamente según el modelo (FR-002, FR-003, FR-017; SC-009).
- [ ] T013 [US1] Añadir en tests/test_interfaz.py registro, validación, nombre más color, confirmación/cancelación, rechazo de borrado y avisos accesibles a 360/1280 con teclado (FR-002, FR-017; UI-001 a UI-005).

### Implementación y cierre

- [ ] T014 [US1] Definir normalización NFC, nombre_clave por casefold y paleta en app/reglas.py y esquema estricto de materia en app/schemas.py, con límites y mensajes del contrato (FR-002, FR-003, FR-013).
- [ ] T015 [US1] Implementar consultas de alta/listado/borrado en app/db.py y rutas /api/materias en app/main.py, con confirmación de transacción y rechazo de cualquier materia con tareas (FR-002, FR-003, FR-017).
- [ ] T016 [US1] Incorporar catálogo y formulario de materia en app/static/index.html y app/static/app.js, validación por puntos de código, mensajes por campo, bloqueo de envíos repetidos y confirmación/cancelación de borrado (FR-002, FR-013, FR-017).
- [ ] T017 [US1] Adaptar catálogo, paleta y confirmación en app/static/styles.css con foco visible, nombres accesibles, textos que envuelvan y ausencia de desplazamiento horizontal a ambos anchos (UI-001, UI-002, UI-004).
- [ ] T018 [US1] Añadir en tests/test_persistencia.py conservación de nombre/color y borrado de una materia vacía tras reiniciar la app contra el mismo archivo (FR-012; SC-004).
- [ ] T019 [US1] Ejecutar pruebas compartidas y de US1 y documentar comandos/resultados y revisión de teclado en specs/001-organizar-tareas-academicas/evidencias.md; no cerrar la historia mientras fallen (FR-016; SC-007).

## Fase 4: Historia 2 — Registrar tareas por materia (P1)

**Objetivo**: Crear tareas pendientes válidas con descripción opcional.
**Prueba independiente**: Con una materia preparada, guardar con/sin descripción,
consultar los datos y rechazarlos ante entradas inválidas sin cambios parciales.

### Pruebas automatizadas obligatorias

- [ ] T020 [P] [US2] Ampliar tests/test_reglas.py con título de 0/1/150/151 y descripción de 0/2000/2001 puntos de código, nula/ausente/blanca, NFC/emoji/NUL, tipos incorrectos y fechas imposibles/bisiestas/pasadas (FR-004, FR-013; SC-005).
- [ ] T021 [P] [US2] Ampliar tests/test_api.py con alta/consulta de tareas, materia obligatoria/inexistente, estado inicial pendiente, campos desconocidos, JSON inválido, duplicados de título admitidos y error sin registros parciales (FR-004, FR-005, FR-013).
- [ ] T022 [US2] Ampliar tests/test_interfaz.py con creación con/sin descripción, ausencia de materias, mensajes asociados, conservación del formulario ante fallo y contenido literal a 360/1280 (FR-004, FR-005, FR-011, FR-013; UI-001 a UI-005).

### Implementación y cierre

- [ ] T023 [US2] Implementar reglas de título/descripción/fecha en app/reglas.py y esquema de alta en app/schemas.py: texto normalizado, fechas exactas sin hora, descripción opcional y tipos estrictos según contracts/api.md (FR-004, FR-013).
- [ ] T024 [US2] Implementar en app/db.py alta atómica y consulta de tareas y en app/main.py POST/GET /api/tareas sin filtros aún, devolviendo datos completos ordenados por fecha_entrega/id y errores de materia inexistente (FR-004, FR-005, FR-006).
- [ ] T025 [US2] Incorporar formulario y acceso a descripción completa en app/static/index.html y app/static/app.js, selección de materia, límites en puntos de código, textos literales, mensajes en español y guía para crear materia si no existe (FR-004, FR-005, FR-011, FR-013).
- [ ] T026 [US2] Añadir pruebas de conservación de todos los campos y estado de tareas en tests/test_persistencia.py y estilos adaptables del formulario en app/static/styles.css (FR-012; SC-004; UI-001).
- [ ] T027 [US2] Ejecutar pruebas compartidas, US1 y US2 y registrar comandos/resultados y revisión de teclado en specs/001-organizar-tareas-academicas/evidencias.md (FR-016; SC-007).

## Fase 5: Historia 3 — Consultar entregas y prioridades (P1)

**Objetivo**: Listado ordenado con alertas textuales de vencimiento y urgencia.
**Prueba independiente**: Con tareas preparadas y reloj controlado, comprobar orden,
fronteras temporales y actualización, sin depender de formularios de alta.

### Pruebas automatizadas obligatorias

- [ ] T028 [US3] Añadir en tests/test_api.py casos de listado vacío y tareas con fechas empatadas, inserción desordenada y datos completos; exigir orden por fecha y luego id (FR-005, FR-006, FR-011; SC-002).
- [ ] T029 [US3] Añadir en tests/test_interfaz.py pruebas de la función temporal JavaScript con reloj controlado a 48 horas ±1 ms y vencimiento ±1 ms, completadas sin alertas, fin de mes/año, zona America/La_Paz y cambio estacional (FR-007; SC-003).
- [ ] T030 [US3] Añadir en tests/test_interfaz.py pruebas de actualización activa en menos de 60 segundos y recálculo al volver por foco/visibilidad, listado vacío y etiquetas accesibles en ambos anchos (FR-011, FR-015; UI-001 a UI-005).

### Implementación y cierre

- [ ] T031 [US3] Implementar en app/static/app.js función temporal pura con instante inyectable, medianoche local del siguiente día por calendario, diferencia real de 172800000 ms y prioridad de completada/vencida/urgente; conservar fecha original (FR-007).
- [ ] T032 [US3] Implementar en app/static/app.js actualización cada 30 segundos y al recuperar foco/visibilidad, recalculando antes de presentar la vista recuperada (FR-015).
- [ ] T033 [US3] Completar listado y estado vacío en app/static/index.html y app/static/app.js con título, materia por nombre/color, fecha, estado, descripción consultable y alertas textuales; distinguir error de recuperación de lista vacía y permitir reintento (FR-005, FR-006, FR-007, FR-011, FR-014).
- [ ] T034 [US3] Definir en app/static/styles.css jerarquía legible para fechas/alertas y textos extensos, sin depender de color/tachado ni desbordar a 360/1280 (UI-001, UI-004).
- [ ] T035 [US3] Ejecutar todas las pruebas existentes y registrar resultados y revisión manual de prioridades/listado en specs/001-organizar-tareas-academicas/evidencias.md; identificar US1+US2+US3 como primera entrega mínima útil (FR-016; SC-007).

## Fase 6: Historia 4 — Completar tareas (P2)

**Objetivo**: Conservar tareas completadas y retirar sus alertas.
**Prueba independiente**: Completar una tarea preparada y repetir la operación;
comprobar estado, conservación, ausencia de alertas y persistencia.

### Pruebas automatizadas obligatorias

- [ ] T036 [P] [US4] Añadir en tests/test_api.py casos PATCH /api/tareas/{id}/completar, inexistente, identificador inválido e idempotencia sin alterar otros campos (FR-008).
- [ ] T037 [P] [US4] Añadir en tests/test_persistencia.py reapertura con tareas completadas y todos sus datos intactos (FR-008, FR-012; SC-004).
- [ ] T038 [US4] Añadir en tests/test_interfaz.py completado accesible, aviso y retirada de alertas temporales a 360/1280, sin ocultar el estado por depender solo de tachado (FR-008; UI-001 a UI-005).

### Implementación y cierre

- [ ] T039 [US4] Implementar actualización idempotente en app/db.py y ruta PATCH /api/tareas/{id}/completar en app/main.py según el contrato, sin reapertura ni borrado de tareas (FR-008).
- [ ] T040 [US4] Incorporar controles de completar en app/static/index.html y app/static/app.js y representación de estado en app/static/styles.css; actualizar solo tras éxito, conservar datos ante error y anunciar el resultado (FR-008, FR-014; UI-003, UI-004).
- [ ] T041 [US4] Ejecutar la batería acumulada y registrar comandos/resultados en specs/001-organizar-tareas-academicas/evidencias.md (FR-016; SC-007).

## Fase 7: Historia 5 — Filtrar tareas (P2)

**Objetivo**: Combinar filtros de materia/estado manteniendo el orden.
**Prueba independiente**: Preparar dos materias con tareas pendientes/completadas;
comprobar filtros individuales, combinados, vacíos y restablecimiento.

### Pruebas automatizadas obligatorias

- [ ] T042 [US5] Añadir en tests/test_api.py filtros materia_id/estado, parámetros ausentes, valores inválidos, materia inexistente, intersección y orden constante con agenda de cinco materias y cien tareas (FR-009, FR-013; SC-002).
- [ ] T043 [US5] Añadir en tests/test_interfaz.py filtros a 360/1280, valores iniciales, restablecimiento, sin coincidencias, desaparición al completar bajo Pendientes y borrado de materia filtrada conservando estado (FR-009, FR-010, FR-011, FR-017; UI-001 a UI-005).

### Implementación y cierre

- [ ] T044 [US5] Ampliar app/main.py y app/db.py con validación de filtros y consulta parametrizada por intersección, manteniendo ORDER BY fecha_entrega/id y errores en español (FR-009, FR-013).
- [ ] T045 [US5] Añadir selectores y acción de restablecer en app/static/index.html, app/static/app.js y app/static/styles.css con valores iniciales Todas/Todas las materias, resultados sin coincidencias y anuncios accesibles (FR-009, FR-010, FR-011; UI-001 a UI-003).
- [ ] T046 [US5] Integrar en app/static/app.js actualización de resultados al completar tareas y de selectores al borrar materia activa, conservando filtro de estado y orden; probar errores sin sustituir la agenda por un vacío (FR-008, FR-009, FR-017).
- [ ] T047 [US5] Ejecutar todas las pruebas acumuladas y documentar resultados y revisión de teclado de filtros en specs/001-organizar-tareas-academicas/evidencias.md (FR-016; SC-007).

## Fase 8: Revisión transversal y entrega

- [ ] T048 Ampliar tests/test_interfaz.py con un recorrido integral de las cinco historias a 360/1280 y comprobaciones de etiquetas, errores asociados, foco visible, avisos, contenido literal y ausencia de desplazamiento horizontal (UI-001 a UI-005; SC-006).
- [ ] T049 Añadir en tests/test_interfaz.py medición de completar/filtrar con cinco materias y cien tareas contra el límite de un segundo de SC-008; registrar condiciones y resultado en specs/001-organizar-tareas-academicas/evidencias.md (SC-008).
- [ ] T050 Ampliar tests/test_api.py y tests/test_interfaz.py con errores de lectura/escritura/bloqueo, reintento, cero cambios parciales y conservación de formularios; comprobar validación equivalente en cliente y servidor, sin depender solo del cliente (FR-013, FR-014; SC-005).
- [ ] T051 Revisar nombres, funciones pequeñas, dependencias mínimas, ausencia de capas superfluas y comentarios de decisiones no obvias en app/main.py, app/db.py, app/schemas.py, app/reglas.py y app/static/app.js; registrar revisión en specs/001-organizar-tareas-academicas/evidencias.md (constitución I y III).
- [ ] T052 Realizar la revisión manual de teclado, lector de pantalla, foco, legibilidad, errores y confirmación de borrado a 360/1280 y documentar resultados en specs/001-organizar-tareas-academicas/evidencias.md (UI-001 a UI-005; SC-006, SC-007).
- [ ] T053 Evaluar registro de materia y primera tarea con cinco estudiantes, registrar tiempos y asistencia en specs/001-organizar-tareas-academicas/evidencias.md y contrastar al menos cuatro sin ayuda en dos minutos (SC-001).
- [ ] T054 Ejecutar python -m pytest sobre toda la batería, registrar cantidad, comando, fecha y resultado en specs/001-organizar-tareas-academicas/evidencias.md; añadir pruebas de regresión para cada error corregido y exigir resultado satisfactorio antes de finalizar (FR-016; SC-007).
- [ ] T055 Actualizar instrucciones verificadas en specs/001-organizar-tareas-academicas/quickstart.md, revisar documentación en español y registrar el cumplimiento final de criterios y los dos checklists en specs/001-organizar-tareas-academicas/evidencias.md, sin marcar controles pendientes como aprobados (FR-014, FR-016).

## Dependencias y orden de ejecución

```text
Preparación (T001–T004)
    → Fundamentos (T005–T010)
        → US1 (T011–T019)
            → US2 (T020–T027)
                → US3 (T028–T035)
                    → US4 (T036–T041)
                        → US5 (T042–T047)
                            → Revisión y entrega (T048–T055)
```

- Orden predeterminado: secuencial por identificador salvo los pares independientes indicados.
- T002/T003 dependen de T001. T004 revisa requisitos antes de comenzar historias;
  una carencia relevante se documenta y acuerda antes de implementar su solución.
- T005 precede a T006; T007 usa esos fundamentos. T008 permite T009 y las pruebas
  posteriores; T010 integra el esqueleto de interfaz con la aplicación.
- En cada historia, definir primero sus pruebas; implementarla después y ejecutar
  todas las pruebas pertinentes antes de cerrar su tarea de verificación.
- US2 requiere materias; US3 requiere tareas. US4 usa listado y alertas. US5 integra
  los cambios de US1/US4. Los datos preparados permiten probar cada historia por
  separado sin simular su resultado como si ya existiera implementación.
- No trabajar simultáneamente en historias que comparten app/main.py, app/db.py,
  app/static/app.js o los mismos archivos de pruebas. Mantener los cambios de esos
  archivos en secuencia incluso si varias personas participan.
- T053 requiere participantes reales; si no están disponibles, la evaluación queda
  pendiente y no se declara SC-001 satisfecho. No se sustituyen personas por automatización.

## Oportunidades y ejemplos de trabajo en paralelo

Los pares siguientes modifican archivos distintos, después de completar sus
prerrequisitos; `[P]` no autoriza anticipar una dependencia pendiente.

| Fase o historia | Ejemplo permitido | Ejecución restante |
|-----------------|-------------------|--------------------|
| Preparación | T002 y T003 después de T001 | T004 antes de historias |
| US1 | T011 y T012 después de fundamentos | T013–T019 secuenciales |
| US2 | T020 y T021 después de US1 | T022–T027 secuenciales |
| US3 | Sin par [P]; T029 y T030 comparten archivo | T028–T035 secuenciales |
| US4 | T036 y T037 después de US3 | T038–T041 secuenciales |
| US5 | Sin par [P]; pruebas e integración comparten archivos | T042–T047 secuenciales |

## Estrategia de implementación

Entregar primero US1 como catálogo verificable, y después US2+US3 para obtener la
primera agenda mínima útil. US4 y US5 completan la versión solicitada; no son
opcionales. Probar cada incremento, mantener documentación en español y no introducir
cuentas, borrado de tareas, reapertura de completadas, Docker ni microservicios.

## Trazabilidad y finalización

| Requisitos o criterios | Tareas principales |
|-----------------------|--------------------|
| FR-001 | T007, T010 |
| FR-002, FR-003 | T011–T017 |
| FR-004, FR-005 | T020–T026, T028, T033 |
| FR-006 | T024, T028, T033 |
| FR-007, FR-015 | T029–T032 |
| FR-008 | T036–T040, T043, T046 |
| FR-009, FR-010 | T042–T046 |
| FR-011 | T022, T025, T028, T030, T033, T043, T045 |
| FR-012 | T005, T006, T009, T018, T026, T037 |
| FR-013 | T006, T011–T016, T020–T025, T042, T044, T050 |
| FR-014 | T007, T010, T033, T040, T050, T055 |
| FR-016 | T002, T019, T027, T035, T041, T047, T054, T055 |
| FR-017 | T005, T012, T013, T015, T016, T043, T046 |
| SC-001 | T053 |
| SC-002 | T028, T042 |
| SC-003 | T029–T032 |
| SC-004 | T009, T018, T026, T037 |
| SC-005 | T011, T020–T025, T042, T050 |
| SC-006 | T013, T022, T030, T038, T043, T048, T052 |
| SC-007 | T019, T027, T035, T041, T047, T052, T054 |
| SC-008 | T030, T032, T049 |
| SC-009 | T012, T013, T015, T043, T046 |
| UI-001 a UI-005 | Pruebas de interfaz por historia, T048 y T052 |

Todas las tareas permanecen pendientes hasta disponer de su resultado verificable.
La existencia de tareas o una casilla marcada no sustituye pruebas satisfactorias.
