# Plan de implementación: [NOMBRE DE LA FUNCIONALIDAD]

**Rama**: `[###-nombre-funcionalidad]` | **Fecha**: [FECHA] | **Especificación**: [enlace]
**Entrada**: `/specs/[###-nombre-funcionalidad]/spec.md`

**Nota**: `/speckit-plan` completa esta plantilla. Redactar todo el contenido en español.

## Resumen

[Requisito principal, alcance mínimo y enfoque técnico seleccionado]

## Contexto técnico

**Lenguaje y versión**: [valor o REQUIERE ACLARACIÓN]
**Dependencias principales**: [solo las necesarias para el alcance actual]
**Almacenamiento**: [solución o no aplica]
**Pruebas**: [herramientas, niveles necesarios y comandos de ejecución]
**Plataforma objetivo**: [plataforma; incluir celular y computadora para la interfaz]
**Tipo de proyecto**: [tipo y justificación]
**Objetivos de rendimiento**: [métricas vinculadas a requisitos actuales]
**Restricciones**: [límites técnicos y académicos]
**Escala y alcance**: [usuarios, datos y flujos previstos]

## Comprobación de la constitución

Obligatoria antes de la investigación de la fase 0 y después del diseño de la fase 1.
Registrar evidencia o referencias para cada control.

- [ ] Simplicidad: el diseño cubre requisitos actuales; cada dependencia y capa es necesaria.
- [ ] Pruebas: cada funcionalidad tiene pruebas automatizadas previstas y un comando reproducible.
- [ ] Legibilidad: nombres claros, funciones pequeñas y documentación de decisiones no obvias.
- [ ] Validación: cada entrada tiene reglas, punto de validación y casos válidos, inválidos y límite.
- [ ] Interfaz: flujos verificables a 360 y 1280 píxeles, teclado, foco y etiquetas accesibles.
- [ ] Idioma: todos los documentos están redactados en español.

[Registrar resultado inicial y resultado posterior al diseño; explicar no aplicables.
Un incumplimiento bloquea la finalización. Una funcionalidad sin interfaz puede
justificar que las comprobaciones de interfaz no aplican.]

## Estructura del proyecto

### Documentación de la funcionalidad

```text
specs/[###-nombre-funcionalidad]/
├── plan.md          # Este plan
├── research.md      # Investigación de la fase 0
├── data-model.md    # Modelo de datos de la fase 1, si corresponde
├── quickstart.md    # Guía de ejecución y pruebas de la fase 1
├── contracts/       # Contratos de la fase 1, si corresponden
└── tasks.md         # Tareas generadas por /speckit-tasks
```

### Código fuente

[Reemplazar el siguiente ejemplo por la estructura mínima real. No crear capas sin necesidad.]

```text
src/
tests/
```

**Decisión de estructura**: [explicar directorios elegidos y su necesidad]

## Seguimiento de complejidad

Completar solo cuando haya complejidad adicional que justificar según el principio I.
No permite omitir pruebas, validación, legibilidad ni accesibilidad.

| Complejidad adicional | Necesidad actual | Por qué no basta una alternativa más simple |
|----------------------|------------------|---------------------------------------------|
| [decisión] | [requisito] | [razón verificable] |
