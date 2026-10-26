---
description: "Plantilla de tareas para implementar una funcionalidad"
---

# Tareas: [NOMBRE DE LA FUNCIONALIDAD]

**Entrada**: Documentos de `/specs/[###-nombre-funcionalidad]/`
**Requisitos previos**: plan.md y spec.md; research.md, data-model.md y contracts/ cuando correspondan.
**Pruebas**: OBLIGATORIAS para toda funcionalidad. Incluir pruebas automatizadas
por historia, casos límite, entradas inválidas y regresiones pertinentes.
**Organización**: Agrupar por historia para permitir implementación y verificación independientes.
**Idioma**: Redactar todo el contenido en español.

## Formato: `[ID] [P?] [Historia] Descripción`

- Identificadores consecutivos: T001, T002 y siguientes.
- **[P]**: Tarea ejecutable en paralelo porque modifica archivos distintos y no tiene dependencias pendientes.
- **[US1]**, **[US2]**: Historia asociada; obligatorio en tareas de historias.
- Incluir rutas exactas de archivos y dependencias cuando correspondan.

## Convenciones de rutas

- Proyecto único: `src/` y `tests/`.
- Aplicación web: `backend/src/`, `frontend/src/` y sus directorios de pruebas.
- Adaptar las rutas al plan; no crear infraestructura ni capas sin necesidad actual.

<!-- Las tareas siguientes son ejemplos. /speckit-tasks debe sustituirlas por tareas
concretas derivadas de las historias, requisitos, entidades y contratos existentes.
Conservar la cobertura de los cinco principios y eliminar ejemplos no aplicables. -->

## Fase 1: Preparación

**Propósito**: Preparar solo las herramientas necesarias para el alcance actual.

- [ ] T001 Crear la estructura mínima de directorios definida en plan.md
- [ ] T002 Configurar dependencias y ejecución del proyecto en [ruta de configuración]
- [ ] T003 [P] Configurar pruebas automatizadas y su comando en [ruta de configuración de pruebas]
- [ ] T004 [P] Configurar formato y análisis de código en [ruta de configuración]

## Fase 2: Fundamentos compartidos

**Propósito**: Resolver únicamente requisitos que bloqueen las historias.

- [ ] T005 Implementar [requisito compartido indispensable] en [ruta exacta]
- [ ] T006 Verificar automáticamente [comportamiento compartido] en [ruta de prueba]

**Punto de control**: Las dependencias necesarias están listas y sus pruebas pasan.
Omitir esta fase si no existen fundamentos compartidos.

## Fase 3: Historia de usuario 1 - [Título] (Prioridad: P1)

**Objetivo**: [valor mínimo entregado]
**Prueba independiente**: [acción, resultado esperado y comando]

### Pruebas automatizadas de la historia 1 (obligatorias)

- [ ] T007 [P] [US1] Crear pruebas de aceptación y lógica para [comportamiento] en [ruta de prueba]
- [ ] T008 [P] [US1] Crear pruebas de entradas válidas, inválidas y límite en [ruta de prueba]
- [ ] T009 [US1] Crear pruebas de integración para [interacción real, si existe] en [ruta de prueba]
- [ ] T010 [US1] Crear pruebas de flujos a 360 y 1280 píxeles y accesibilidad automatizable en [ruta de prueba de interfaz, si existe]

### Implementación de la historia 1

- [ ] T011 [US1] Implementar [capacidad mínima] en [ruta exacta] con nombres claros y funciones pequeñas
- [ ] T012 [US1] Validar [entradas] antes de procesarlas y devolver errores claros en [ruta exacta]
- [ ] T013 [US1] Adaptar [interfaz] a celular y computadora con teclado, foco y etiquetas en [ruta exacta, si existe interfaz]
- [ ] T014 [US1] Documentar decisiones no obvias y ejecución en [ruta de documentación]
- [ ] T015 [US1] Ejecutar pruebas nuevas y existentes y registrar comando y resultado en [ruta de evidencia]
- [ ] T016 [US1] Verificar manualmente teclado y presentación en ambos tamaños y registrar evidencia en [ruta, si existe interfaz]

**Punto de control**: La historia cumple sus criterios de aceptación, las pruebas
pasan y la documentación está en español. Solo entonces puede marcarse terminada.

## Fase 4: Historia de usuario 2 - [Título] (Prioridad: P2)

[Repetir la estructura anterior con identificadores consecutivos y etiqueta US2.
Añadir únicamente historias requeridas por la especificación. Cada historia debe
incluir sus pruebas automatizadas, implementación, validaciones y evidencia.]

## Fase final: Revisión transversal

- [ ] TXXX Revisar simplicidad, nombres, responsabilidades y decisiones no obvias en [rutas modificadas]
- [ ] TXXX [P] Actualizar la documentación en español en [rutas de documentación]
- [ ] TXXX Ejecutar toda la batería de pruebas y registrar comando y resultado en [ruta de evidencia]
- [ ] TXXX Comprobar los cinco principios y criterios de aceptación en [ruta de lista de verificación]
- [ ] TXXX Validar los pasos de ejecución de quickstart.md, si existe

## Dependencias y orden de ejecución

- Preparar herramientas antes de ejecutar las historias que dependan de ellas.
- Resolver los fundamentos necesarios antes de las historias afectadas.
- Crear pruebas por historia y ejecutarlas contra la implementación; ninguna
  historia termina sin pruebas automatizadas satisfactorias.
- Completar modelos antes de servicios y servicios antes de sus consumidores,
  únicamente si esas capas existen en el plan.
- Las correcciones de errores incorporan pruebas de regresión.
- La revisión final depende de todas las historias incluidas en la entrega.

## Oportunidades de trabajo en paralelo

Las tareas marcadas [P] pueden ejecutarse simultáneamente cuando no modifiquen
los mismos archivos ni dependan de resultados pendientes. Documentar dependencias
entre historias; no asumir independencia si comparten componentes en desarrollo.

## Estrategia de implementación

1. Completar preparación y fundamentos necesarios.
2. Entregar primero la historia P1 como producto mínimo viable.
3. Verificar criterios de aceptación, pruebas, validación e interfaz de esa historia.
4. Incorporar las siguientes historias por prioridad sin romper pruebas existentes.
5. Registrar evidencia y completar la revisión transversal antes de finalizar.

## Notas

- Sustituir todos los ejemplos y rutas pendientes por valores concretos.
- No introducir tareas para necesidades hipotéticas.
- No sustituir pruebas automatizadas por demostraciones manuales.
- No marcar tareas dependientes como completadas mientras falle su verificación.
