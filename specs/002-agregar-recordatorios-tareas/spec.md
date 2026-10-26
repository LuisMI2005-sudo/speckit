# Especificación de funcionalidad: Recordatorios de tareas pendientes

**Rama**: `002-agregar-recordatorios-tareas`
**Creación**: 2026-10-26
**Estado**: Lista para planificación
**Entrada**: Agregar recordatorios: el estudiante recibe una notificación un día
antes de la fecha de entrega de cada tarea pendiente.

Extensión del [organizador académico de la UPB](../001-organizar-tareas-academicas/spec.md),
sujeta a la constitución 1.0.0. Los identificadores de este documento pertenecen
exclusivamente a esta funcionalidad. Todo el contenido se redacta en español.

## Aclaraciones

### Sesión 2026-10-26

- Pregunta: ¿Dónde recibe el recordatorio? → Respuesta: Notificación del navegador
  mientras la agenda esté abierta.
- Pregunta: ¿Cuándo significa un día antes? → Respuesta: A las 09:00 del día anterior
  a la fecha de entrega, según la hora local del dispositivo.

## Escenarios de usuario y pruebas (obligatorio)

### Historia de usuario 1 - Habilitar recordatorios (Prioridad: P1)

Como estudiante, quiero permitir las notificaciones y conocer si están disponibles
para decidir si puedo contar con los recordatorios de mi agenda.

**Motivo de la prioridad**: Sin permiso no es posible emitir el aviso del navegador.
**Prueba independiente**: Verificar automáticamente los estados de permiso y los
mensajes de disponibilidad, sin necesitar tareas ni esperar una fecha real.

**Escenarios de aceptación**:

1. **Dado** que no se ha decidido el permiso, **Cuando** abre la agenda, **Entonces**
   encuentra «Activar recordatorios» y una explicación de horario y necesidad de
   mantener la agenda abierta, sin una solicitud automática de permiso.
2. **Dado** un entorno compatible, **Cuando** activa recordatorios y concede permiso,
   **Entonces** se informa que los recordatorios están disponibles en ese navegador.
3. **Dado** que rechaza o cierra la solicitud sin conceder permiso, **Cuando** vuelve
   a la agenda, **Entonces** se explica que no se emitirán notificaciones, sin
   bloquear materias, tareas, filtros ni las alertas de urgencia existentes.
4. **Dado** que el permiso está denegado o el entorno no admite notificaciones,
   **Cuando** consulta el estado, **Entonces** ve la causa en español y, cuando
   corresponda, orientación para revisar permisos; no se insiste automáticamente.

### Historia de usuario 2 - Recibir el aviso previo a la entrega (Prioridad: P1)

Como estudiante, quiero recibir un aviso de cada tarea pendiente el día anterior
para recordar el trabajo antes de que llegue su fecha de entrega.

**Motivo de la prioridad**: Es el valor principal solicitado.
**Prueba independiente**: Preparar tareas y permiso concedido; controlar la fecha
local y comprobar la emisión, contenido y exclusión de tareas no elegibles.

**Escenarios de aceptación**:

1. **Dado** una tarea pendiente con entrega el 2026-10-28 y la agenda abierta,
   compatible y con permiso, **Cuando** son las 09:00 locales del 2026-10-27,
   **Entonces** se emite su recordatorio en un máximo de 60 segundos.
2. **Dado** una tarea cuyo aviso corresponde hoy, **Cuando** son las 08:59:59,
   **Entonces** todavía no se emite; a las 09:00 comienza su ventana de emisión.
3. **Dado** varias tareas elegibles, **Cuando** se evalúan los recordatorios,
   **Entonces** se emite uno por tarea, identificando título, materia y fecha de entrega.
4. **Dado** una tarea completada antes de emitir el aviso, **Cuando** llega su horario,
   **Entonces** no se emite ningún recordatorio de esa tarea.
5. **Dado** una tarea con entrega hoy, pasada o posterior a mañana, **Cuando** se
   evalúa a las 09:00, **Entonces** no recibe un recordatorio de esta funcionalidad.
6. **Dado** dos tareas con igual título pero identidades distintas, **Cuando** ambas
   resultan elegibles, **Entonces** cada una recibe su propio recordatorio.

### Historia de usuario 3 - Evitar avisos repetidos o desactualizados (Prioridad: P2)

Como estudiante, quiero que abrir de nuevo la agenda no repita los recordatorios
ni me avise sobre trabajos que ya completé.

**Motivo de la prioridad**: Evita distracciones y avisos que contradigan el estado actual.
**Prueba independiente**: Preparar un recordatorio ya emitido y otro pendiente;
reabrir la agenda y simular cambios de estado, horario y fallos conocidos.

**Escenarios de aceptación**:

1. **Dado** un recordatorio emitido, **Cuando** se recarga la agenda, se reabre o
   se evalúa desde otra pestaña de la misma instalación, **Entonces** no se repite
   el recordatorio de esa tarea y fecha de entrega.
2. **Dado** una agenda cerrada a las 09:00, **Cuando** se abre a las 15:00 de ese
   mismo día con permiso disponible, **Entonces** se emiten los recordatorios
   pendientes de hoy en un máximo de 60 segundos.
3. **Dado** un aviso no emitido el día anterior, **Cuando** abre la agenda durante
   el día de entrega o después, **Entonces** no se genera ese recordatorio atrasado.
4. **Dado** una tarea creada después de las 09:00 del día previo a su entrega,
   **Cuando** se guarda y sigue pendiente, **Entonces** recibe el aviso dentro
   de la ventana de hoy, sin esperar al siguiente día.
5. **Dado** un fallo conocido al emitir o falta de datos actuales, **Cuando** se
   evalúa un aviso, **Entonces** no se declara emitido y se informa el problema;
   un reintento posterior solo procede dentro de la ventana y si sigue pendiente.
6. **Dado** una tarea completada antes de reintentar, **Cuando** se recupera la
   disponibilidad, **Entonces** se cancela el recordatorio todavía no emitido.

### Casos límite

- Cambio de mes, año o año bisiesto: el día anterior es una fecha de calendario,
  no necesariamente las últimas 24 horas transcurridas.
- Cambios de zona horaria o reloj: se recalcula el horario local; un aviso ya
  emitido para esa tarea y fecha no se repite al retroceder el reloj.
- Pestaña suspendida o dispositivo dormido: no se garantiza puntualidad mientras
  no pueda funcionar; al recuperar actividad se aplica la ventana del día actual.
- Permiso concedido después de las 09:00: emitir pendientes solo dentro de la
  ventana del mismo día. Permiso revocado: detener nuevas emisiones y mostrar el estado.
- Varias pestañas o perfiles contra la misma instalación: conservar una sola emisión
  por tarea/fecha en uso normal, sin identificar usuarios ni crear cuentas.
- Tarea completada mientras se prepara el recordatorio: volver a comprobar su
  estado antes de autorizar la emisión; una notificación ya emitida no se deshace.
- Si la emisión anterior queda con resultado incierto por un cierre o fallo, no
  reenviar automáticamente como si se conociera el fracaso; registrar la incertidumbre.
- Un título largo o con apariencia de instrucciones sigue siendo texto literal;
  el aviso no incluye la descripción opcional y los datos completos siguen en la agenda.

## Requisitos (obligatorio)

### Requisitos funcionales

- **FR-001**: La agenda DEBE ofrecer la activación explícita de notificaciones,
  explicando horario, alcance y necesidad de mantenerla abierta antes de solicitar
  permiso. Aceptación: historia 1.1 y 1.2.
- **FR-002**: La agenda DEBE comunicar permiso disponible, no concedido, denegado
  o notificaciones no disponibles, sin bloquear las funciones existentes ni insistir
  automáticamente. Aceptación: historia 1.3 y 1.4.
- **FR-003**: Cada tarea pendiente DEBE tener un recordatorio elegible desde las
  09:00 locales del día anterior a su fecha de entrega. Aceptación: historia 2.1 y 2.2.
- **FR-004**: La ventana para emitir ese recordatorio DEBE terminar al comenzar la
  fecha de entrega, a las 00:00 locales; fuera de ella no se emiten avisos atrasados.
  Aceptación: historia 2.5 y 3.2 a 3.4.
- **FR-005**: Con agenda activa, entorno compatible, datos actuales y permiso
  disponible, la emisión DEBE ocurrir en un máximo de 60 segundos desde que el
  aviso sea elegible o se recuperen esas condiciones. Aceptación: historia 2.1 y 3.2.
- **FR-006**: El recordatorio DEBE ser una notificación del navegador que identifique
  título de tarea, nombre de materia y fecha de entrega en español; no debe incluir
  su descripción. Aceptación: historia 2.3 y casos límite de contenido.
- **FR-007**: La aplicación DEBE excluir tareas completadas y volver a comprobar
  el estado antes de emitir. Completar cancela avisos aún no emitidos, pero no exige
  retirar una notificación anterior. Aceptación: historia 2.4 y 3.6.
- **FR-008**: La aplicación DEBE conservar el resultado de emisión para evitar
  repeticiones de la misma tarea/fecha al recargar, reiniciar o usar varias pestañas
  o perfiles de la instalación. Cada tarea distinta conserva su propio aviso.
  Aceptación: historia 3.1 y 2.6.
- **FR-009**: Al abrir o recuperar la agenda, conceder permiso o registrar una tarea,
  la aplicación DEBE reevaluar avisos elegibles que todavía no se emitieron dentro
  de la ventana vigente. Aceptación: historia 3.2 a 3.4 y casos límite de permiso.
- **FR-010**: Los fallos conocidos o datos no disponibles NO DEBEN marcar un aviso
  como emitido ni producir confirmaciones falsas; los reintentos DEBEN respetar
  fecha, estado y deduplicación. Un resultado incierto no se reenvía automáticamente.
  Aceptación: historia 3.5 y 3.6 y caso límite de resultado incierto.
- **FR-011**: La hora de recordatorio DEBE calcularse como día anterior a las 09:00
  en la zona local vigente, respetando cambios de calendario. El cambio de zona
  no modifica la fecha de entrega guardada ni repite avisos emitidos. Aceptación:
  casos límite de calendario y reloj.
- **FR-012**: Los recordatorios DEBEN conservar las reglas existentes de materias,
  tareas, filtros, persistencia y urgencia. No modifican la fecha ni el estado de
  una tarea. Aceptación: regresión de la agenda base y escenarios de esta extensión.
- **FR-013**: Todo dato recibido para evaluar o actualizar un recordatorio DEBE
  validarse antes de procesarse: tarea existente, fecha válida, estado permitido
  y resultado de emisión permitido. Ante error, conservar tareas y datos anteriores.
  Aceptación: tabla de validación.
- **FR-014**: Toda funcionalidad nueva DEBE contar con pruebas automatizadas de
  aceptación, límites, fallos y regresión antes de finalizar. Registrar comando
  reproducible y resultados, con revisión manual complementaria de accesibilidad.

#### Reglas temporales y significado de emisión

Para una entrega el 2026-10-28, el horario objetivo es el 2026-10-27 a las 09:00
locales y la ventana termina el 2026-10-28 a las 00:00. No es «24 horas antes del
fin del día de entrega». La alerta «Urgente» de la agenda base sigue usando sus
48 horas y es independiente del recordatorio.

«Emitido» significa que el navegador aceptó la solicitud de notificación; no implica
que el estudiante la leyó ni que el sistema operativo garantice mostrarla. Los
requisitos de puntualidad aplican con la agenda activa y sin suspensión ni bloqueos
del sistema. No se requiere emisión mientras la agenda esté cerrada.

### Validación de entradas

No se añaden campos configurables de horario ni datos de contacto. Se reutilizan
los límites de nombre de materia 1–100, título 1–150 y descripción 0–2000, con NFC
y las reglas de la especificación base.

| Dato | Reglas y límites | Respuesta ante error | Escenarios automatizados |
|------|------------------|---------------------|--------------------------|
| Tarea referida | Identidad existente en la agenda | No emitir ni modificar datos ajenos | Existente, ausente e inexistente |
| Fecha de entrega | Fecha de calendario válida, sin hora | No programar con fecha inválida | Fin de mes/año, bisiesto, fecha imposible |
| Estado de tarea | Pendiente o completada; solo pendiente es elegible | Excluir completadas y rechazar estado desconocido | Pendiente, completada e inválido |
| Permiso | Estado actual informado por el navegador | Informar indisponibilidad; no simular autorización | Concedido, sin decidir, denegado, revocado |
| Resultado de emisión | No emitido, emitido o incierto | Rechazar valor desconocido; conservar resultado anterior | Cada estado, repetición y valor inválido |
| Contenido del aviso | Título y materia válidos, fecha asociada; texto literal | No incluir descripción ni ejecutar contenido | Longitudes máximas, tildes, emoji y texto especial |

### Accesibilidad y adaptación de la interfaz

- **UI-001**: Activación, estado de permisos y mensajes de recordatorios DEBEN
  funcionar a 360 y 1280 píxeles sin pérdida de contenido, superposición ni
  desplazamiento horizontal de la página.
- **UI-002**: Los controles DEBEN tener etiquetas y operación por teclado con foco
  visible; los avisos de permiso y fallo DEBEN ser perceptibles con lector de
  pantalla y no depender solo del color.
- **UI-003**: La agenda DEBE mostrar el estado de disponibilidad en texto aunque
  no se puedan emitir notificaciones. No se afirmará que este mensaje sustituye
  una notificación del navegador ni que el usuario ya la recibió.
- **UI-004**: Se DEBEN automatizar las comprobaciones de los flujos principales en
  ambos tamaños y complementar con revisión manual de permisos, foco y presentación
  en los entornos compatibles que se determinen durante la planificación.

### Entidades principales (si existen datos)

- **Tarea y materia**: Entidades existentes; se conservan identidad, fecha, estado,
  títulos y nombres. No se añaden contactos ni usuarios.
- **Recordatorio**: Seguimiento de una tarea y su fecha de entrega, horario local
  derivado y resultado de emisión, conservado para evitar duplicados.
- **Disponibilidad de notificaciones**: Capacidad y permiso del navegador actual;
  no debe tratarse como un permiso global transferible a otros perfiles.

## Criterios de éxito (obligatorio)

### Resultados medibles

- **SC-001**: Con veinte tareas preparadas y reloj controlado, el 100 % de las
  pendientes elegibles recibe una solicitud de notificación dentro de 60 segundos
  en las condiciones de disponibilidad definidas; ninguna completada o fuera de
  ventana la recibe.
- **SC-002**: Tras diez reevaluaciones, una recarga, una reapertura y consultas
  simultáneas desde dos contextos de la misma instalación, no hay solicitudes
  repetidas por tarea/fecha emitida en funcionamiento normal.
- **SC-003**: Todos los casos justo antes, exactamente en y después de las 09:00,
  así como del inicio del día de entrega, cumplen las reglas de la ventana.
- **SC-004**: El 100 % de los casos sin permiso, con permiso revocado, incompatibilidad
  o fallo muestra el estado real sin perder datos ni bloquear la agenda.
- **SC-005**: Los flujos de activación y consulta de disponibilidad son accesibles
  con teclado y utilizables a 360 y 1280 píxeles sin los defectos descritos en UI-001.
- **SC-006**: Todas las pruebas nuevas y existentes pasan antes de finalizar, con
  evidencia reproducible; fallos, calendario y deduplicación cuentan con cobertura.

## Supuestos y alcance mínimo

- Esta funcionalidad amplía la agenda 001, cuya primera versión excluía recordatorios.
  Esa exclusión se refiere a la entrega base y no impide esta extensión solicitada.
- Se mantienen Python 3.12, FastAPI, SQLite y frontend sin frameworks como restricciones
  ya acordadas; el diseño de recordatorios corresponde a un plan nuevo. La agenda
  base todavía no está implementada y constituye una dependencia de esta extensión.
- El horario fijo es 09:00 del día anterior; no se incluyen preferencias horarias,
  posposición, recurrencias, correo, SMS, mensajería ni notificaciones remotas.
- Se requiere agenda abierta y una instalación local disponible. No se promete
  entrega con aplicación cerrada, dispositivo dormido o pestaña suspendida; al
  recuperar actividad se aplica la ventana vigente y se omiten recordatorios antiguos.
- El navegador y sistema operativo controlan permisos y presentación. La planificación
  debe identificar entornos compatibles en celular y computadora y un acceso que
  permita notificaciones; donde falten capacidades se informa sin bloquear la agenda.
- La puntualidad se mide con reloj controlado y condiciones explícitas de disponibilidad.
  La lectura humana y la entrega garantizada por el sistema operativo no forman parte
  del criterio de éxito. No se modifica la regla existente de «Urgente».
- El alcance no incluye implementar la agenda ni los recordatorios durante este comando.

La consideración de permisos y compatibilidad se apoya en la
[guía oficial de notificaciones del navegador](https://developer.mozilla.org/en-US/docs/Web/API/Notifications_API/Using_the_Notifications_API).
