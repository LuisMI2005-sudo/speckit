# Especificación de funcionalidad: [NOMBRE DE LA FUNCIONALIDAD]

**Rama**: `[###-nombre-funcionalidad]`
**Creación**: [FECHA]
**Estado**: Borrador
**Entrada**: Descripción del usuario: "$ARGUMENTS"

Redactar todo el contenido en español y cumplir `.specify/memory/constitution.md`.

## Escenarios de usuario y pruebas (obligatorio)

<!-- Priorizar historias como P1, P2 y P3. Cada historia debe aportar valor y ser
verificable de forma independiente. Añadir o eliminar historias según el alcance real. -->

### Historia de usuario 1 - [Título breve] (Prioridad: P1)

[Describir el recorrido del usuario y el valor que obtiene]

**Motivo de la prioridad**: [justificación]
**Prueba independiente**: [acción, resultado observable y prueba automatizada prevista]

**Escenarios de aceptación**:

1. **Dado** [estado inicial], **Cuando** [acción], **Entonces** [resultado esperado].
2. **Dado** [entrada inválida], **Cuando** [acción], **Entonces** [rechazo claro sin cambios parciales].

### Historia de usuario 2 - [Título breve] (Prioridad: P2)

[Describir el recorrido; eliminar esta historia si no es necesaria]

**Motivo de la prioridad**: [justificación]
**Prueba independiente**: [acción, resultado observable y prueba automatizada prevista]

**Escenarios de aceptación**:

1. **Dado** [estado inicial], **Cuando** [acción], **Entonces** [resultado esperado].

### Casos límite

- [Valores vacíos, formatos incorrectos y límites pertinentes]
- [Errores de dependencias o interacciones relevantes para el alcance]

## Requisitos (obligatorio)

### Requisitos funcionales

- **FR-001**: El sistema DEBE [capacidad mínima verificable].
- **FR-002**: El sistema DEBE [comportamiento y resultado observable].

[Usar REQUIERE ACLARACIÓN con una explicación cuando falte una decisión esencial.]

### Validación de entradas

| Dato de usuario | Reglas y límites | Comportamiento ante error | Escenarios automatizados |
|-----------------|------------------|---------------------------|--------------------------|
| [dato] | [presencia, tipo, formato, longitud, rango y dominio] | [mensaje y rechazo] | [válido, inválido y límite] |

Validar antes de procesar o persistir. Si existe servidor, validar también en él.

### Accesibilidad y adaptación de la interfaz

- **UI-001**: Los flujos principales DEBEN funcionar a 360 y 1280 píxeles sin pérdida
  de contenido, superposición de controles ni desplazamiento horizontal de la página.
- **UI-002**: La interfaz DEBE permitir navegación por teclado con foco visible,
  etiquetas y errores asociados a campos, estructura semántica e información que
  no dependa exclusivamente del color.
- [Identificar flujos, resultados esperados y verificaciones automatizadas y manuales.
  Si no existe interfaz, justificar que esta sección no aplica.]

### Entidades principales (si existen datos)

- **[Entidad]**: [significado, atributos y relaciones sin imponer una implementación].

## Criterios de éxito (obligatorio)

### Resultados medibles

- **SC-001**: [resultado de usuario medible, independiente de la tecnología].
- **SC-002**: Cada funcionalidad tiene pruebas automatizadas de aceptación, límites
  y errores pertinentes; las pruebas nuevas y existentes pasan antes de finalizar.
- **SC-003**: [resultado verificable de los flujos principales en celular y computadora].

## Supuestos y alcance mínimo

- [Supuestos sobre usuarios, datos y entorno]
- [Límites actuales y funciones aplazadas; no excluir celular ni pruebas obligatorias]
- [Dependencias existentes que se reutilizan y motivo]
