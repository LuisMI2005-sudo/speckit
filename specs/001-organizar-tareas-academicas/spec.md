# Especificación de funcionalidad: Organizador de tareas académicas de la UPB

**Rama**: `001-organizar-tareas-academicas`
**Creación**: 2026-10-26
**Estado**: Lista para planificación
**Entrada**: Aplicación para estudiantes de la UPB que permite registrar materias
con nombre y color; crear tareas por materia con título, descripción opcional y
fecha de entrega; consultar tareas por fecha con vencidas destacadas y urgentes
en las próximas 48 horas; completarlas y filtrarlas por materia o estado.
Primera versión para un usuario por dispositivo, sin inicio de sesión.

Esta especificación se rige por la constitución 1.0.0 del proyecto. Todo su
contenido y los documentos derivados deben estar en español.

## Aclaraciones

### Sesión 2026-10-26

- Pregunta: ¿Qué pasa al borrar una materia? → Respuesta: Solo se permite borrar
  materias sin tareas; cualquier tarea, pendiente o completada, bloquea el borrado.
- Pregunta: ¿Qué límites de longitud fijamos? → Respuesta: Nombre de materia de
  1 a 100 caracteres, título de 1 a 150 y descripción opcional de hasta 2000;
  recortar espacios exteriores de nombre y título y rechazar excesos sin truncar.

- Pregunta: ¿Cómo se calcula «Urgente»? → Respuesta: Solo para pendientes cuando
  faltan más de 0 y hasta 48 horas inclusive para el fin de la fecha de entrega
  local; al alcanzar ese límite pasa a «Vencida». Las completadas no reciben alertas.

## Escenarios de usuario y pruebas (obligatorio)

### Historia de usuario 1 - Registrar y borrar materias vacías (Prioridad: P1)

Como estudiante, quiero registrar el nombre y el color de mis materias para
reconocer a qué asignatura corresponde cada tarea.

**Motivo de la prioridad**: Las materias organizan las tareas y son un requisito
para crearlas. Esta historia entrega un catálogo utilizable de asignaturas.
**Prueba independiente**: Registrar una materia y verificar automáticamente su
nombre y color al consultarla y al volver a abrir la aplicación.

**Escenarios de aceptación**:

1. **Dado** un estudiante sin materias, **Cuando** registra «Cálculo I» con un color
   disponible, **Entonces** la materia aparece con ese nombre y color y puede
   seleccionarse al crear tareas.
2. **Dado** el formulario de materia, **Cuando** se intenta guardar un nombre vacío,
   compuesto solo de espacios o mayor al límite, o un color inválido, **Entonces**
   se muestra el error asociado al campo y no se crea la materia.
3. **Dado** que existe «Cálculo I», **Cuando** intenta registrar « cálculo i »,
   **Entonces** se informa que la materia ya existe y se evita el duplicado.
4. **Dado** que existen materias guardadas, **Cuando** se cierra y vuelve a abrir la
   aplicación en la misma instalación del dispositivo, **Entonces** se conservan sus
   nombres y colores.

5. **Dado** una materia sin tareas, **Cuando** confirma su borrado, **Entonces**
   la materia desaparece del catálogo y de los selectores, sin afectar otras materias.
6. **Dado** una materia con al menos una tarea pendiente o completada, **Cuando**
   intenta borrarla, **Entonces** se muestra «No puedes borrar una materia con tareas»,
   se conserva la materia y no se modifica ni elimina ninguna tarea.
7. **Dado** una materia vacía, **Cuando** cancela la confirmación de borrado,
   **Entonces** no cambia ningún dato.

### Historia de usuario 2 - Registrar tareas por materia (Prioridad: P1)

Como estudiante, quiero registrar una tarea y su fecha de entrega dentro de una
materia para recordar mis compromisos académicos.

**Motivo de la prioridad**: Es la capacidad central del organizador y permite
construir una primera entrega útil junto con las historias 1 y 3.
**Prueba independiente**: Partiendo de una materia existente, crear tareas con y
sin descripción y comprobar automáticamente los datos guardados y su asociación.

**Escenarios de aceptación**:

1. **Dado** que existe «Cálculo I», **Cuando** registra «Resolver práctica 1», esa
   materia y una fecha válida, sin descripción, **Entonces** se guarda una tarea
   pendiente con los datos indicados.
2. **Dado** un formulario válido, **Cuando** añade una descripción y guarda,
   **Entonces** puede consultar la descripción completa desde la tarea.
3. **Dado** un formulario con título vacío, materia inexistente o fecha inválida,
   **Cuando** intenta guardar, **Entonces** se señalan los campos inválidos, se
   conservan los datos ingresados y no se crea ninguna tarea.
4. **Dado** que no hay materias, **Cuando** intenta crear una tarea, **Entonces** se
   explica que primero debe registrar una materia y se ofrece acceso a ese flujo.
5. **Dado** que la fecha de entrega ya pasó, **Cuando** guarda una tarea válida,
   **Entonces** se admite el registro y la tarea se muestra como vencida.
6. **Dado** que existen tareas guardadas, **Cuando** vuelve a abrir la aplicación,
   **Entonces** se conservan materia, título, descripción, fecha y estado.

### Historia de usuario 3 - Consultar entregas y prioridades (Prioridad: P1)

Como estudiante, quiero ver mis tareas en orden de entrega e identificar cuáles
están vencidas o son urgentes para decidir qué atender primero.

**Motivo de la prioridad**: Transforma los registros en una agenda que ayuda a
priorizar el trabajo académico.
**Prueba independiente**: Con tareas preparadas y una hora de referencia controlada,
comprobar automáticamente el orden, las etiquetas y los límites de 48 horas.

**Escenarios de aceptación**:

1. **Dado** un conjunto de tareas ingresadas en distinto orden, **Cuando** consulta
   el listado, **Entonces** se muestran por fecha de entrega ascendente y cada una
   indica título, materia por nombre y color, fecha y estado.
2. **Dado** una tarea pendiente cuyo plazo terminó, **Cuando** consulta el listado,
   **Entonces** aparece destacada con la etiqueta textual «Vencida» y no «Urgente».
3. **Dado** una tarea pendiente a la que restan exactamente 48 horas, **Cuando**
   consulta el listado, **Entonces** aparece con la etiqueta «Urgente»; si restan
   más de 48 horas, no aparece esa etiqueta.
4. **Dado** una tarea pendiente cuyo plazo se alcanza en este instante, **Cuando**
   se evalúa su clasificación, **Entonces** aparece como «Vencida».
5. **Dado** una tarea completada con fecha pasada o cercana, **Cuando** se muestra,
   **Entonces** se identifica como «Completada» sin etiquetas de vencimiento o urgencia.
6. **Dado** una aplicación abierta mientras transcurre el tiempo, **Cuando** una
   tarea cruza el límite de urgencia o vencimiento, **Entonces** su clasificación
   se actualiza en un máximo de 60 segundos mientras la vista está activa; al
   volver a ella se recalcula antes de mostrarla.
7. **Dado** que no existen tareas, **Cuando** abre el listado, **Entonces** se
   muestra un mensaje en español y la acción para crear la primera tarea.

### Historia de usuario 4 - Marcar tareas como completadas (Prioridad: P2)

Como estudiante, quiero marcar una tarea terminada para distinguir el trabajo
realizado del que todavía tengo pendiente.

**Motivo de la prioridad**: Permite mantener vigente la agenda sin borrar el historial.
**Prueba independiente**: Con una tarea pendiente preparada, completarla y verificar
automáticamente su estado, persistencia y exclusión del filtro de pendientes.

**Escenarios de aceptación**:

1. **Dado** una tarea pendiente, **Cuando** la marca como completada, **Entonces**
   se conserva con todos sus datos, cambia a «Completada» y pierde las etiquetas
   «Urgente» o «Vencida» que tuviera.
2. **Dado** una tarea completada, **Cuando** vuelve a abrir la aplicación,
   **Entonces** la tarea mantiene su estado completado.
3. **Dado** el filtro «Pendientes» activo, **Cuando** completa una tarea visible,
   **Entonces** esta deja de aparecer y se confirma la acción en español.
4. **Dado** una tarea ya completada, **Cuando** se repite la acción de completar,
   **Entonces** no se duplica la tarea ni cambia su información.

### Historia de usuario 5 - Filtrar tareas (Prioridad: P2)

Como estudiante, quiero filtrar por materia y estado para concentrarme en una
asignatura o revisar lo pendiente y lo completado.

**Motivo de la prioridad**: Facilita consultar agendas con tareas de varias materias.
**Prueba independiente**: Preparar dos materias con tareas pendientes y completadas;
verificar automáticamente los filtros individuales, combinados y sin resultados.

**Escenarios de aceptación**:

1. **Dado** tareas de varias materias, **Cuando** elige una materia, **Entonces** solo
   se muestran las tareas de esa materia respetando el orden por fecha.
2. **Dado** tareas pendientes y completadas, **Cuando** elige «Pendientes»,
   «Completadas» o «Todas», **Entonces** ve exactamente las tareas de ese estado.
3. **Dado** una materia y un estado seleccionados, **Cuando** consulta el listado,
   **Entonces** solo aparecen tareas que cumplen ambas condiciones.
4. **Dado** filtros sin coincidencias, **Cuando** consulta el listado, **Entonces**
   ve «No hay tareas para estos filtros» y puede restablecerlos sin perder datos.
5. **Dado** filtros activos, **Cuando** los restablece, **Entonces** se seleccionan
   «Todas las materias» y «Todas» y reaparece el listado completo ordenado.

### Casos límite

- Una materia con tareas completadas también bloquea el borrado. Si se crea una tarea
  durante el intento de borrar su materia, se preserva la integridad: nunca queda
  una tarea huérfana. Se prueba además cancelar y borrar una materia inexistente.
- Si se borra la materia actualmente filtrada, el filtro cambia a «Todas las materias»
  conservando el estado seleccionado; se informa el resultado y se actualizan selectores.

- Los campos obligatorios no admiten solo espacios. Se recortan espacios exteriores
  de nombres y títulos antes de validar y guardar; se conservan tildes y caracteres españoles.
- Se prueban longitudes mínima, máxima y un carácter por encima del máximo.
- Un nombre de materia repetido se compara sin distinguir mayúsculas ni espacios
  exteriores; las tildes se conservan y distinguen. Dos materias pueden compartir color.
- Dos tareas pueden compartir título, materia y fecha; no se consideran duplicados
  automáticamente. A igual fecha, se conserva el orden de creación, la más antigua primero.
- Se admite una fecha pasada y se rechaza una fecha inexistente, como el 30 de febrero.
- Se verifican los instantes a ambos lados y exactamente en los límites de 48 horas
  y vencimiento, el cambio de día y el cambio de zona horaria del dispositivo.
- Una tarea completada nunca se resalta como urgente ni vencida, incluso al cambiar la hora.
- Si guardar falla, se informa que no se guardó, se mantienen los datos del formulario
  y no se confirma éxito ni se alteran parcialmente los registros existentes.
- Si no se pueden recuperar los datos, se informa el problema y se permite reintentar;
  no se sobrescriben automáticamente con una agenda vacía.
- Los textos largos y caracteres con apariencia de instrucciones se presentan como
  contenido literal, sin ejecutar acciones ni romper la presentación.

## Requisitos (obligatorio)

### Requisitos funcionales

- **FR-001**: La aplicación DEBE permitir su uso inmediato sin cuenta, contraseña
  ni inicio de sesión, con una sola agenda por instalación local del dispositivo.
- **FR-002**: El estudiante DEBE poder registrar materias con nombre y color
  obligatorios y consultar las materias registradas. Aceptación: historia 1.
- **FR-003**: La aplicación DEBE impedir nombres de materia duplicados según las
  reglas de validación. El color no tiene que ser único. Aceptación: historia 1.3.
- **FR-004**: El estudiante DEBE poder crear una tarea asociada a exactamente una
  materia existente, con título y fecha de entrega obligatorios y descripción
  opcional; toda tarea nueva comienza pendiente. Aceptación: historia 2.
- **FR-005**: La aplicación DEBE permitir consultar todos los datos de una tarea,
  incluida su descripción cuando exista. Aceptación: historias 2.2 y 3.1.
- **FR-006**: El listado DEBE ordenar todas las tareas visibles por fecha de entrega
  ascendente y, en caso de empate, por orden de creación ascendente. Aceptación: historia 3.1.
- **FR-007**: Las tareas pendientes DEBEN clasificarse como vencidas, urgentes o
  sin alerta mediante las reglas temporales indicadas más abajo. Las etiquetas
  «Vencida» y «Urgente» son mutuamente excluyentes. Aceptación: historias 3.2 a 3.4.
- **FR-008**: El estudiante DEBE poder marcar una tarea pendiente como completada.
  Deben conservarse sus datos y excluirse las alertas temporales de las tareas
  completadas. Aceptación: historias 3.5 y 4.
- **FR-009**: La aplicación DEBE ofrecer un filtro por una materia o «Todas las
  materias» y otro por estado «Todas», «Pendientes» o «Completadas». Los filtros
  DEBEN combinarse por intersección y mantener el orden de entrega. «Urgente» y
  «Vencida» son alertas de pendientes, no estados adicionales. Aceptación: historia 5.
- **FR-010**: Al abrir la aplicación o restablecer los filtros, DEBEN seleccionarse
  «Todas las materias» y «Todas». Aceptación: historia 5.5.
- **FR-011**: La aplicación DEBE distinguir una agenda vacía de una consulta sin
  coincidencias y ofrecer la acción apropiada sin eliminar registros. Aceptación:
  historias 2.4, 3.7 y 5.4.
- **FR-012**: Las materias, tareas y estados guardados DEBEN conservarse tras cerrar
  y volver a abrir la aplicación en la misma instalación local del dispositivo. No se exige
  sincronización entre dispositivos o instalaciones. Aceptación: historias 1.4, 2.6 y 4.2.
- **FR-013**: Todo dato del usuario DEBE validarse antes de procesarse o guardarse,
  con errores claros en español, sin pérdida de los campos ingresados ni cambios
  parciales. Aceptación: historias 1.2, 1.3, 2.3 y casos límite de guardado fallido.
- **FR-014**: Toda la interfaz y documentación DEBEN estar en español. Los fallos de
  guardado o recuperación DEBEN comunicarse sin afirmar éxito ni borrar datos.
  Aceptación: casos límite de fallos y revisión de los flujos de las historias 1 a 5.
- **FR-015**: La clasificación temporal DEBE recalcularse al abrir o volver al
  listado y en un máximo de 60 segundos después de cruzar un límite mientras
  permanezca activo. Aceptación: historia 3.6.
- **FR-016**: Cada funcionalidad DEBE tener pruebas automatizadas de sus escenarios
  de aceptación, límites y errores pertinentes antes de darse por terminada;
  la entrega DEBE registrar el comando reproducible y resultados satisfactorios
  de las pruebas nuevas y existentes. Las revisiones manuales complementan estas pruebas.

- **FR-017**: El estudiante DEBE poder borrar una materia solo si no tiene tareas,
  después de confirmar la acción. Una tarea pendiente o completada bloquea el
  borrado; no existe borrado en cascada ni tareas sin materia. Cancelar no cambia
  datos. Si una materia filtrada se borra, se restablece «Todas las materias» y se
  conserva el filtro de estado. Aceptación: historias 1.5 a 1.7 y prueba de filtro activo.

#### Reglas de fecha, vencimiento y urgencia

La fecha de entrega es una fecha de calendario sin hora introducida por el usuario.
El estudiante dispone de todo ese día. Se define el **límite de entrega** como el
inicio del día siguiente a las 00:00 en la zona horaria local del dispositivo.
La misma fecha guardada se interpreta en la zona local vigente al consultar.

| Condición | Clasificación visible |
|-----------|-----------------------|
| La tarea está completada | Completada, sin alerta temporal |
| Está pendiente y el instante actual es igual o posterior al límite de entrega | Vencida |
| Está pendiente y faltan más de 0 y hasta 48 horas inclusive para el límite | Urgente |
| Está pendiente y faltan más de 48 horas para el límite | Pendiente, sin alerta |

Las 48 horas representan tiempo transcurrido, no dos fechas de calendario. La
fecha de entrega visible no cambia aunque cambie la zona horaria del dispositivo.
La regla de orden por fecha también se aplica al consultar tareas completadas.

### Validación de entradas

Estos límites fueron confirmados para la primera versión y se aplican
antes de guardar. Los máximos incluyen espacios interiores y signos de puntuación.
No se truncan silenciosamente los textos. Para contar de forma consistente se
normalizan a Unicode NFC y se cuentan puntos de código, no bytes; un emoji simple
cuenta como un carácter y una secuencia compuesta puede contar como varios.
La descripción conserva su contenido, salvo que solo contenga espacios: se guarda vacía.
Se rechaza el carácter NUL en los campos de texto para mantener la validación coherente.

| Dato de usuario | Reglas y límites | Comportamiento ante error | Escenarios automatizados |
|-----------------|------------------|---------------------------|--------------------------|
| Nombre de materia | Entre 1 y 100 caracteres tras recortar espacios exteriores; único sin distinguir mayúsculas | «Ingresa un nombre de materia de 1 a 100 caracteres» o «Esta materia ya existe» | Vacío, espacios, 1, 100, 101 caracteres, duplicado con mayúsculas y espacios |
| Color de materia | Una selección obligatoria de los colores ofrecidos por la aplicación | «Selecciona un color válido» | Selección válida, ausente y valor ajeno a las opciones |
| Materia de tarea | Una materia registrada y existente | «Selecciona una materia existente» | Materia válida, ausente e inexistente |
| Título de tarea | Entre 1 y 150 caracteres tras recortar espacios exteriores | «Ingresa un título de 1 a 150 caracteres» | Vacío, espacios, 1, 150 y 151 caracteres |
| Descripción | Opcional, hasta 2000 caracteres; si solo contiene espacios se considera vacía | «La descripción no puede superar los 2000 caracteres» | Ausente, vacía, espacios, 2000 y 2001 caracteres |
| Fecha de entrega | Fecha de calendario existente y obligatoria; se admiten días pasados, presentes y futuros | «Ingresa una fecha de entrega válida» | Ausente, imposible, año bisiesto y fechas pasada, presente y futura |
| Filtro de materia | «Todas las materias» o una materia existente | «Selecciona una materia existente»; no aplicar un filtro inválido | Opción general, existente e inexistente |
| Filtro de estado | «Todas», «Pendientes» o «Completadas» | «Selecciona un estado válido»; no aplicar un filtro inválido | Cada opción y valor no admitido |

La validación cubre todo punto de recepción de datos. Si la solución incorporase
un servidor, este también debe validar aunque la interfaz ya lo haya hecho.

### Accesibilidad y adaptación de la interfaz

- **UI-001**: Registrar materias, crear y consultar tareas, completarlas y usar
  filtros DEBE ser posible a anchos de 360 y 1280 píxeles sin perder contenido,
  superponer controles ni desplazar horizontalmente la página.
- **UI-002**: Todos los flujos DEBEN ser operables con teclado, con foco visible,
  orden de navegación coherente, estructura semántica y etiquetas en los campos.
- **UI-003**: Los errores DEBEN asociarse al campo correspondiente. Los resultados
  de guardado, completado y filtrado DEBEN ser perceptibles también para quienes
  usan lectores de pantalla.
- **UI-004**: Las materias DEBEN identificarse por nombre además del color; las
  alertas DEBEN incluir texto «Vencida» o «Urgente», y el estado completado DEBE
  reconocerse sin depender exclusivamente de color o tachado.
- **UI-005**: Las pruebas automatizadas DEBEN cubrir los flujos principales en ambos
  anchos y las comprobaciones de accesibilidad automatizables. La revisión manual
  DEBE verificar teclado, foco, legibilidad y presentación visual en ambos tamaños.

### Entidades principales (si existen datos)

- **Materia**: Asignatura del estudiante. Tiene identidad propia, nombre y color;
  puede existir sin tareas y puede estar asociada a varias tareas.
- **Tarea**: Compromiso académico con identidad propia, una materia obligatoria,
  título, descripción opcional, fecha de entrega, estado pendiente o completado
  y orden de creación para resolver empates. La alerta temporal es derivada del
  estado, fecha y hora de referencia; no es un estado editable por el estudiante.

## Criterios de éxito (obligatorio)

### Resultados medibles


- **SC-001**: En una evaluación con cinco estudiantes, al menos cuatro registran
  una materia y su primera tarea sin asistencia en un máximo de dos minutos.
- **SC-002**: En una agenda de referencia con cinco materias y cien tareas, el 100 %
  de las tareas aparece en el orden requerido y los filtros individuales y
  combinados devuelven exactamente las coincidencias esperadas.
- **SC-003**: El 100 % de los casos de frontera temporal —más de 48 horas,
  exactamente 48 horas, menos de 48 horas, límite de entrega y plazo vencido—
  muestra la clasificación correcta; ninguna tarea completada recibe alerta.
- **SC-004**: Tras cerrar y volver a abrir la aplicación en la misma instalación, se
  recupera el 100 % de las materias y tareas guardadas con todos sus datos y estados.
- **SC-005**: El 100 % de las entradas inválidas de la tabla de validación se rechaza
  con un mensaje asociado y sin guardar registros parciales ni perder los campos válidos.
- **SC-006**: Los cinco flujos principales, incluido el borrado de materias vacías, se completan a 360 y 1280 píxeles y con
  teclado, sin bloqueo, pérdida de contenido, superposición ni desplazamiento
  horizontal; materia, alerta y estado se distinguen sin depender del color.
- **SC-007**: El 100 % de los escenarios de aceptación y errores pertinentes tiene
  pruebas automatizadas satisfactorias antes de la entrega, con comando y
  resultados documentados; la comprobación manual de accesibilidad queda registrada.
- **SC-008**: En la agenda de referencia, tras completar una tarea o cambiar un
  filtro, el resultado visible se actualiza en un máximo de un segundo durante
  el uso habitual; las alertas temporales respetan el máximo de 60 segundos.

- **SC-009**: El 100 % de los intentos de borrar materias con tareas se rechaza sin
  modificar registros; borrar una materia vacía solo elimina esa materia y cancelar
  conserva todos los datos. Se verifica también la actualización del filtro activo.

## Supuestos y alcance mínimo

- El único actor es el estudiante de la UPB. No hay cuentas, roles, matrícula,
  contraseñas ni verificación de afiliación institucional.
- Con el almacenamiento SQLite indicado para la planificación, se usa una agenda
  por instalación local. Los navegadores que acceden a esa misma instancia comparten
  agenda; otro perfil no crea una agenda independiente. No existe sincronización
  entre instalaciones ni identificación de usuarios.
- La conservación cubre cierres del navegador y reinicios de la aplicación mientras
  se conserve el archivo de datos de la instalación. Borrar datos del navegador no
  borra la agenda. Borrar el archivo sí la elimina; no se incluyen copias de respaldo
  ni recuperación de datos borrados por el usuario.
- La fecha no incluye hora de entrega. Se confirman fin de día local, reloj del
  dispositivo y los límites de texto confirmados en esta sesión.
- Los colores se eligen de opciones ofrecidas por la aplicación; no se necesita
  introducir códigos de color ni garantizar colores únicos entre materias.
- Al abrir y al restablecer filtros se muestra la agenda completa. Conservar la
  selección de filtros después de cerrar no forma parte de esta versión.
- El alcance incluye registrar, consultar y borrar materias sin tareas; crear, consultar y completar
  tareas; ordenar, destacar y filtrar. No incluye editar registros ni eliminar tareas,
  reabrir tareas completadas, subtareas, adjuntos, recurrencias, notificaciones,
  calendario externo, importación, exportación ni colaboración.
- Todas las historias son obligatorias para esta primera versión; las prioridades
  indican orden de entrega, no funciones opcionales. La historia 2 necesita una
  materia existente y las historias 3 a 5 necesitan tareas; se pueden verificar
  aisladamente con datos preparados que cumplan esas condiciones.
- Las únicas dependencias externas al contenido son un dispositivo con fecha y
  zona horaria configuradas y capacidad de conservar los datos. No se requiere
  integración con servicios institucionales. La planificación usa Python 3.12, FastAPI y SQLite, con HTML, CSS y JavaScript
  sin frameworks servidos por FastAPI; pytest para pruebas, un solo proyecto,
  sin Docker ni microservicios.
