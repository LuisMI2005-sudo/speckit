<!--
Informe de sincronización
- Versión anterior: plantilla sin ratificar → 1.0.0 (primera adopción).
- Principios establecidos: I. Simplicidad primero; II. Pruebas obligatorias;
  III. Código legible; IV. Validación de entradas; V. Accesible y responsivo.
- Secciones añadidas: Idioma y contexto académico; Flujo de trabajo y criterios de
  finalización; Gobernanza.
- Secciones eliminadas: ninguna; se sustituyeron los marcadores de la plantilla.
- Archivos sincronizados:
  - .specify/templates/constitution-template.md: actualizado en español.
  - .specify/templates/plan-template.md: actualizado con controles de los cinco principios.
  - .specify/templates/spec-template.md: actualizado con requisitos verificables.
  - .specify/templates/tasks-template.md: actualizado con pruebas obligatorias.
  - .specify/templates/checklist-template.md: actualizado en español.
  - .agents/skills/speckit-tasks/SKILL.md: corregida la condición de pruebas opcionales.
  - AGENTS.md: actualizado con idioma y precedencia de la constitución.
- .specify/templates/commands/: no existe en este proyecto; se revisaron las
  instrucciones locales de generación de tareas e implementación.
- No existen README.md ni docs/quickstart.md del proyecto para sincronizar.
- Pendientes: ninguno.
-->
# Constitución del proyecto académico de la UPB

## Principios fundamentales

### I. Simplicidad primero

Se DEBE implementar la solución mínima que satisfaga los requisitos actuales y sus
criterios de aceptación. No se DEBEN añadir funciones, dependencias, capas ni
abstracciones para necesidades hipotéticas (YAGNI: no lo vas a necesitar).
Toda complejidad adicional DEBE justificarse en el plan con una necesidad actual y
la razón por la que una alternativa más simple no basta. El alcance académico y
el tiempo disponible orientan las decisiones sin reducir los controles de calidad.

### II. Pruebas obligatorias

Toda funcionalidad DEBE contar con pruebas automatizadas antes de darse por
terminada. Las pruebas DEBEN verificar los criterios de aceptación, los casos
límite y los errores pertinentes, incluidas las entradas inválidas. Las
correcciones de errores DEBEN incorporar una prueba de regresión.
Se DEBEN usar pruebas unitarias para lógica aislada y pruebas de integración
cuando el comportamiento dependa de la interacción entre componentes.
La entrega DEBE incluir el comando reproducible de ejecución y evidencia de que
las pruebas nuevas y existentes pasan. Una comprobación manual no sustituye las
pruebas automatizadas.

### III. Código legible

El código DEBE usar nombres claros y coherentes con el dominio y funciones pequeñas
con una responsabilidad definida. Se DEBEN evitar duplicaciones y estructuras
innecesariamente difíciles de entender. Los comentarios y la documentación DEBEN
explicar decisiones, restricciones y comportamientos no obvios, sin repetir lo que
el código ya expresa. La revisión DEBE comprobar que otro integrante pueda entender
el cambio y ejecutar sus pruebas con la documentación disponible.

### IV. Validación de entradas

Todo dato proporcionado por el usuario DEBE validarse antes de procesarlo,
persistirlo o utilizarlo en operaciones del sistema. La validación DEBE comprobar,
según corresponda, presencia, tipo, formato, longitud, rango y reglas del dominio.
En aplicaciones con servidor, este DEBE validar los datos aunque la interfaz ya
los haya validado. Los datos inválidos DEBEN rechazarse con mensajes claros en
español y sin producir cambios parciales ni revelar información interna.
Las pruebas automatizadas DEBEN cubrir valores válidos, inválidos y límites.

### V. Accesible y responsivo

La interfaz DEBE permitir completar los flujos principales tanto en celular como
en computadora. Se DEBEN verificar al menos anchos de 360 y 1280 píxeles, sin
pérdida de contenido, controles superpuestos ni desplazamiento horizontal de la
página en los flujos principales. La interfaz DEBE usar estructura semántica,
etiquetas en formularios, navegación por teclado, foco visible y mensajes de error
asociados a los campos. La información no DEBE depender exclusivamente del color.
Las pruebas automatizadas DEBEN cubrir los flujos principales en ambos tamaños
y las comprobaciones de accesibilidad automatizables; la revisión manual de
teclado y presentación visual complementa estas pruebas.

## Idioma y contexto académico

Todo el contenido de los documentos del proyecto DEBE estar en español, incluidos
especificaciones, planes, tareas, listas de verificación, informes, comentarios y
guías. Se conservan nombres de archivos, comandos, identificadores técnicos y
nombres propios cuando su traducción impida su uso correcto.

Las decisiones y los resultados DEBEN ser trazables a los requisitos académicos
acordados. Las fuentes y recursos externos utilizados DEBEN atribuirse en la
documentación pertinente. Esta constitución define acuerdos del proyecto; no
presupone políticas institucionales adicionales de la UPB.

## Flujo de trabajo y criterios de finalización

1. Especificar el alcance mínimo, las historias priorizadas, los criterios de
   aceptación, las reglas de validación y los flujos en celular y computadora.
2. Elaborar un plan que compruebe los cinco principios antes de investigar y
   nuevamente después del diseño; justificar toda complejidad adicional.
3. Desglosar cada historia en tareas de implementación y pruebas automatizadas,
   con las verificaciones de validación, accesibilidad y adaptación necesarias.
4. Implementar y revisar nombres, responsabilidades y documentación de lo no obvio.
5. Ejecutar las pruebas automatizadas nuevas y existentes y registrar el comando
   y el resultado; comprobar también teclado y presentación en ambos tamaños.
6. Dar por terminada la funcionalidad únicamente cuando cumpla sus criterios de
   aceptación, pasen todas las pruebas y esté actualizada la documentación en español.

## Gobernanza

Esta constitución prevalece sobre plantillas, instrucciones de generación y
prácticas locales que la contradigan. Cada revisión de cambios DEBE comprobar
su cumplimiento. Un incumplimiento bloquea la finalización hasta corregirse;
una justificación de complejidad no exime de los demás principios.

Las modificaciones DEBEN documentar la motivación, los principios afectados y el
impacto en especificaciones, planes, tareas y código. El equipo responsable del
proyecto DEBE acordar la modificación antes de adoptarla y sincronizar los
artefactos afectados. Toda modificación DEBE actualizar el informe de
sincronización, la versión y la fecha de última modificación.

La versión sigue el esquema MAYOR.MENOR.PARCHE: MAYOR para eliminar o redefinir
principios de forma incompatible; MENOR para añadir principios o ampliar
obligaciones; PARCHE para aclaraciones sin cambio de obligaciones.
La fecha de ratificación se conserva en las modificaciones posteriores.

**Versión**: 1.0.0 | **Ratificación**: 2026-10-26 | **Última modificación**: 2026-10-26
