# Plan de trabajo para dos integrantes

**Proyecto**: Tiny — organizador académico de la UPB  
**Propósito**: repartir las tareas del SDD con límites claros de archivos y una integración ordenada para reducir conflictos de merge.  
**Participantes**: Integrante A e Integrante B son nombres provisionales; reemplazarlos cuando el equipo confirme quiénes son.

Este plan complementa los SDD de [organización de tareas](001-organizar-tareas-academicas/tasks.md) y [recordatorios](002-agregar-recordatorios-tareas/tasks.md). No cambia sus requisitos, dependencias ni criterios de aceptación. La constitución del proyecto y las tareas existentes siguen teniendo prioridad.

## Reglas de colaboración

1. Antes de empezar una fase, ambos revisan sus tareas, el contrato afectado y los archivos que van a cambiar. Si una tarea toca archivos de ambos, se acuerda quién integra y se trabaja por turnos en ese archivo.
2. Cada integrante crea una rama corta desde la rama de funcionalidad acordada, por ejemplo `001/api-materias` o `001/ui-materias`. No se trabaja directamente sobre `main` ni se fuerza un push.
3. Se abren cambios pequeños mediante pull request hacia la rama de funcionalidad, no directamente a `main`. El autor revisa las pruebas y la otra persona revisa el cambio antes de integrarlo.
4. Integrar primero los fundamentos y después las historias en el orden de dependencias de `tasks.md`. No iniciar una historia dependiente hasta integrar y probar su prerrequisito.
5. Actualizar la rama de trabajo con la rama de funcionalidad antes de abrir o actualizar el pull request. Resolver conflictos localmente, revisar el diff completo y volver a ejecutar las pruebas afectadas.
6. No marcar una tarea como terminada hasta que el cambio esté integrado, sus pruebas pasen y la evidencia requerida esté registrada. Mantener las casillas pendientes hasta comprobarlo.
7. Si ambos necesitan cambiar el mismo archivo, detener el trabajo paralelo en ese archivo: el dueño asignado integra primero; el otro espera o trabaja en un archivo independiente.

## Responsables y límites de archivos

| Área | Integrante A — API, datos y reglas | Integrante B — interfaz y navegador |
|---|---|---|
| Responsabilidad principal | SQLite, reglas de dominio del servidor, esquemas, rutas y pruebas de API/persistencia | HTML, CSS, JavaScript del navegador, accesibilidad y pruebas Playwright |
| Archivos de propiedad | `app/db.py`, `app/schemas.py`, `app/reglas.py`, `app/main.py`, `tests/test_api.py`, `tests/test_reglas.py`, `tests/test_persistencia.py`, `tests/test_recordatorios.py` | `app/static/index.html`, `app/static/styles.css`, `app/static/app.js`, `app/static/recordatorios.js`, `app/static/sw.js`, `tests/test_interfaz.py` |
| Entrega | Contratos de API y respuestas estables; informar cambios de contrato antes de implementarlos | Interfaz consumiendo el contrato integrado; no modificar rutas ni esquema para resolver problemas visuales |

Los archivos base compartidos (`requirements*.txt`, `pytest.ini`, `.gitignore`, `tests/conftest.py`, `README.md` y documentos de SDD) se asignan explícitamente en la tabla de fases. Solo su responsable los modifica durante esa fase; la otra persona puede revisar, pero no editar simultáneamente.

## Reparto por fases y tareas

Los identificadores se refieren a las tareas de los documentos enlazados. Este reparto no autoriza saltarse el orden ni completar una tarea sin evidencia.

| Funcionalidad/fase | Integrante A | Integrante B | Integración y control |
|---|---|---|---|
| 001 — preparación T001–T004 | T001 (paquete/dependencias) y T003 (`.gitignore`) | T002 (pytest/guía) y apoyo de revisión del checklist T004 | A integra los archivos de configuración; B actualiza la guía. T004 se acuerda entre ambos antes de las historias. |
| 001 — fundamentos T005–T010 | T005–T007, T009 (base de datos, aplicación y pruebas de persistencia) | T008 y T010 (`conftest.py`, archivos estáticos y pruebas de arranque/interfaz) | T008 es el punto de unión: A entrega la fábrica de app y la forma de inyectar SQLite; B integra el cliente y servidor de navegador. A integra `conftest.py` primero; luego B añade sus fixtures de navegador en un cambio coordinado. |
| 001 — US1, materias T011–T019 | T011, T012, T014, T015, T018 | T013, T016, T017 | A integra y prueba la API antes de que B conecte la interfaz al contrato. T019 se verifica en conjunto; A registra evidencia de API/persistencia y B de navegador/teclado. |
| 001 — US2, tareas T020–T027 | T020, T021, T023, T024, T026 | T022, T025 | A integra reglas y API antes de la interfaz. T026 contiene estilos además de persistencia: A entrega la parte de persistencia; B es dueño de `styles.css`. T027 valida ambos cambios. |
| 001 — US3, consulta T028–T035 | T028 y apoyo de datos de prueba | T029–T034 | A añade pruebas de API/orden. B concentra la lógica de presentación, actualización temporal y accesibilidad en los archivos estáticos. T035 integra secuencialmente. |
| 001 — US4, completar T036–T041 | T036, T037, T039 | T038, T040 | A integra API y persistencia antes del control visual. T041 es validación conjunta. |
| 001 — US5, filtros T042–T047 | T042, T044 | T043, T045, T046 | A integra consulta parametrizada; después B integra filtros de interfaz. T047 prueba la combinación final. |
| 001 — revisión T048–T055 | T050, T051, T054 y evidencia técnica | T048, T049, T052, T053, T055 | T053 requiere participantes reales. Revisar juntos la entrega y no declarar criterios medidos si no se ejecutó la evaluación. |
| 002 — preparación y agenda base T001–T006 | T001, T003, T004 y backend de T006 | T002 y T005; interfaz de T006 | A prepara dependencias y base/API; B prepara navegador e interfaz. T006 se cierra juntos antes de recordatorios. |
| 002 — US1 habilitar T007–T010 | T008 (servidor/servicio) | T007, T009, T010 (pruebas e interfaz) | A entrega el contrato del servicio y B lo consume. Probar permisos concedido, denegado y ausente antes de integrar. |
| 002 — US2 avisos T011–T015 | T011–T013 (reglas, reserva y persistencia) | T014–T015 (programación del navegador y pruebas de interfaz) | Integrar primero reglas y reserva API; después la evaluación del navegador. Revisar conjuntamente que una tarea completada no notifique. |
| 002 — US3 duplicados T016–T019 | T016–T017 (pruebas y autorización/confirmación persistente) | T018–T019 (cliente, recuperación y pruebas de navegador) | A integra primero el estado persistente; B implementa su manejo sin reenviar resultados inciertos. |
| 002 — revisión T020–T022 | T021 y revisión de API/SO | T020 y T022, UI y guía | A y B revisan conjuntamente pruebas, limitaciones del sistema operativo y documentación antes de cerrar. |

### Archivos compartidos que requieren turno de integración

- `app/main.py`: Integrante A es responsable de rutas/servidor. B solicita cambios mediante contrato o PR; A integra el cambio de servidor antes de que B ajuste la interfaz.
- `tests/conftest.py`: Integrante A crea la base temporal y el cliente API; B propone por separado las fixtures de Playwright. Una sola persona integra el archivo por cambio.
- `README.md`, `requirements*.txt`, `pytest.ini` y `evidencias.md`: un único responsable por tarea; evitar ediciones simultáneas y consolidar aportes mediante revisión.
- Los documentos SDD se actualizan por el integrante dueño de la tarea documental. Si hay cambios paralelos, usar archivos diferentes o esperar la integración del primer PR.

## Secuencia de integración

1. Acordar la rama de funcionalidad vigente y confirmar que está actualizada con el remoto.
2. Integrar las tareas de preparación y fundamentos en el orden indicado; ejecutar pruebas compartidas.
3. Para cada historia, integrar primero pruebas/contrato del backend de A; B trabaja en sus archivos estáticos y pruebas de interfaz sin modificar el servidor.
4. Integrar el PR de A y ejecutar pruebas API/persistencia. Luego integrar el PR de B y ejecutar la suite completa, incluida la prueba de navegador afectada.
5. Registrar comandos, resultados, fecha y escenarios en el `evidencias.md` de la funcionalidad. Resolver cualquier discrepancia del SDD mediante acuerdo, no cambiando requisitos unilateralmente.
6. Tras terminar una historia, actualizar la rama de funcionalidad y continuar con la siguiente. Solo el responsable de integración acordado prepara el PR final hacia la rama base.

## Lista breve antes de integrar un PR

- [ ] El PR se limita a tareas asignadas y archivos de propiedad acordados.
- [ ] No modifica ni elimina trabajo de otra persona sin revisión.
- [ ] Incluye pruebas para el comportamiento nuevo, límites y errores.
- [ ] Pasan las pruebas pertinentes y se informa el comando usado.
- [ ] Se revisaron los contratos y no hay cambios incompatibles sin acuerdo.
- [ ] Los conflictos se resolvieron sobre la rama actualizada y se inspeccionó el diff final.
- [ ] La documentación y evidencia están actualizadas; no se marcaron pruebas manuales no realizadas.
