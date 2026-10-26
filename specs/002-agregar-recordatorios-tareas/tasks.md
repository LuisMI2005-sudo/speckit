# Tareas: Recordatorios de tareas pendientes

**Fecha**: 2026-10-26. Documentos de entrada: spec.md, plan.md, research.md,
data-model.md, contracts/api.md y quickstart.md de esta funcionalidad.
**Estado**: Pendiente. Pruebas automatizadas obligatorias. Rutas relativas a la raíz.

## Fase 1: Preparación

- [ ] T001 Configurar Python 3.12, requirements.txt, requirements-dev.txt, pytest.ini y .gitignore con dependencias reproducibles y cachés/datos excluidos.
- [ ] T002 Crear tests/conftest.py con base temporal, cliente API y servidor de navegador aislado a 360/1280; revisar checklist de requisitos de 002 y registrar resultado en specs/002-agregar-recordatorios-tareas/evidencias.md.

## Fase 2: Dependencia de agenda y fundamentos

- [ ] T003 Escribir primero tests/test_api.py para materias, tareas, límites Unicode, completado, filtros, borrado protegido, errores y persistencia (FR-012, FR-013).
- [ ] T004 Implementar agenda mínima en app/main.py, app/db.py y app/reglas.py según el contrato base y el plan de 002, con transacciones y validación estricta (FR-012, FR-013).
- [ ] T005 Implementar app/static/index.html, app/static/styles.css y app/static/app.js con formularios, filtros, alertas de 48 horas, completado, confirmación de borrado, foco y errores en español (FR-012; UI-001 a UI-003).
- [ ] T006 Probar en tests/test_interfaz.py la agenda y conservar SQLite entre instancias en tests/test_api.py; ejecutar la batería base antes de seguir (FR-012; SC-006).

## Fase 3: US1 — Habilitar recordatorios (P1)

Prueba independiente: estados de permiso y capacidad sin tareas preparadas.

- [ ] T007 [US1] Escribir tests/test_interfaz.py para permiso sin decidir, concedido, denegado, revocado y capacidad ausente, sin solicitudes automáticas ni bloqueo de agenda (FR-001, FR-002; SC-004).
- [ ] T008 [US1] Implementar app/static/sw.js y su servicio en app/main.py para registro seguro con alcance raíz y mecanismo de notificación compatible (FR-006).
- [ ] T009 [US1] Implementar activación explícita, estado accesible y detección de capacidad en app/static/recordatorios.js e integración en app/static/index.html (FR-001, FR-002; UI-001 a UI-003).
- [ ] T010 [US1] Comprobar registro real del service worker, teclado y visualización a 360/1280 en tests/test_interfaz.py y registrar evidencia en specs/002-agregar-recordatorios-tareas/evidencias.md.

## Fase 4: US2 — Avisar antes de la entrega (P1)

Prueba independiente: tareas preparadas con reloj controlado; agenda y permiso disponibles.

- [ ] T011 [US2] Escribir tests/test_reglas.py con fronteras de 09:00/00:00, calendario, bisiestos, zonas, tipos y fechas inválidas (FR-003 a FR-005, FR-011, FR-013; SC-003).
- [ ] T012 [US2] Implementar ventana local y validación del contexto temporal en app/reglas.py y app/main.py, sin restar 24 horas como día de calendario (FR-003, FR-004, FR-011).
- [ ] T013 [US2] Implementar reserva atómica y catálogo de estados en app/db.py y app/main.py con veinte tareas de prueba en tests/test_recordatorios.py (FR-005, FR-006, FR-007, FR-008).
- [ ] T014 [US2] Implementar evaluación cada 30 segundos y al abrir/recuperar/guardar/completar en app/static/recordatorios.js y app/static/app.js, enviando solo título/materia/fecha al navegador (FR-005, FR-006, FR-009).
- [ ] T015 [US2] Comprobar veinte avisos elegibles, identidad independiente de títulos, completadas excluidas y límite de 60 segundos en tests/test_interfaz.py y tests/test_recordatorios.py (SC-001, SC-003).

## Fase 5: US3 — Evitar duplicados y avisos antiguos (P2)

Prueba independiente: repetir, reiniciar y consultar desde contextos distintos con estados preparados.

- [ ] T016 [US3] Escribir tests/test_recordatorios.py para reserva concurrente, token desconocido, autorización única, confirmación idempotente y resultados contradictorios (FR-007, FR-008, FR-010, FR-013; SC-002).
- [ ] T017 [US3] Implementar autorización y confirmación persistente en app/db.py y app/main.py: incierto antes de emitir, emitido tras aceptación y no_emitido solo ante fracaso conocido (FR-007, FR-008, FR-010).
- [ ] T018 [US3] Implementar en app/static/recordatorios.js recuperación dentro de ventana, revocación, fallo conocido y resultado incierto sin reenvío; mostrar incertidumbre sin afirmar entrega (FR-009, FR-010).
- [ ] T019 [US3] Verificar diez reevaluaciones, recarga, dos perfiles, cierre/reinicio, apertura tardía, fallo y completado antes de reintento en tests/test_interfaz.py y tests/test_recordatorios.py (SC-002, SC-004).

## Fase 6: Revisión y entrega

- [ ] T020 Revisar foco, permisos, textos, disposición y errores en app/static/index.html y app/static/styles.css mediante navegador; automatizar comprobaciones de accesibilidad a ambos anchos en tests/test_interfaz.py y registrar evidencias de revisión visual (UI-001 a UI-004; SC-005).
- [ ] T021 Ejecutar python -m pytest con todas las pruebas, revisar legibilidad/simplicidad y documentar comandos, resultados y límites de la comprobación del SO en specs/002-agregar-recordatorios-tareas/evidencias.md (FR-014; SC-006; constitución I–V).
- [ ] T022 Actualizar specs/002-agregar-recordatorios-tareas/quickstart.md y README.md con ejecución reproducible, permisos, entorno compatible y limitaciones reales, conservando toda la documentación en español (FR-001, FR-002, FR-014).

## Dependencias, paralelismo y estrategia

Orden de fases: 1 → 2 → US1 → US2 → US3 → revisión. Escribir primero las pruebas
relevantes, comprobar su fallo y completar la implementación antes de cerrar cada
historia. T011 y T016 pueden definirse antes del código al compartir la lógica de
reservas; no dar por completa una historia mientras alguna prueba relevante falle.

No hay tareas marcadas [P]: los módulos compartidos se modifican en secuencia.
Ejemplos por historia: US1 T007→T008→T009→T010; US2 T011→T012→T013→T014→T015;
US3 T016→T017→T018→T019. El primer incremento útil es US1+US2 con agenda base;
US3 es obligatorio para terminar. Los datos de prueba aíslan cada historia.

## Trazabilidad

FR-001/002: T007–T010; FR-003/004/005: T011–T015; FR-006: T008, T013–T015;
FR-007/008: T013, T016–T019; FR-009/010: T014, T017–T019;
FR-011: T011/T012; FR-012: T003–T006; FR-013: T003/T004/T011/T016/T017;
FR-014: T021/T022. SC-001/003: T011/T015; SC-002/004: T007/T016/T019;
SC-005: T010/T020; SC-006: T006/T021. UI-001 a UI-004: T005/T010/T020.
