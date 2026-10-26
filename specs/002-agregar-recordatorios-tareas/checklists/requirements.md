# Lista de verificación de calidad: Recordatorios de tareas pendientes

**Propósito**: Revisar la integridad de los requisitos antes de planificar la extensión.
**Creación**: 2026-10-26
**Funcionalidad**: [Especificación](../spec.md)
**Resultado**: Revisión documental completada; 20 controles satisfactorios.

## Calidad del contenido

- [x] CHK001 El documento describe necesidades y resultados sin imponer algoritmos ni estructura de código.
- [x] CHK002 La notificación aporta valor al estudiante antes de la entrega.
- [x] CHK003 La redacción es comprensible para participantes no técnicos.
- [x] CHK004 Están completas las secciones obligatorias de la plantilla.
- [x] CHK005 El contenido está en español, con rutas y términos técnicos necesarios conservados.

## Integridad de los requisitos

- [x] CHK006 Las dos decisiones esenciales de canal y horario fueron confirmadas por el usuario.
- [x] CHK007 Los requisitos distinguen pendiente/completada y elegibilidad/resultado de emisión.
- [x] CHK008 Los criterios de éxito incluyen cantidades, intervalos y límites medibles.
- [x] CHK009 Los criterios se expresan como resultados y no dependen de un mecanismo concreto.
- [x] CHK010 Las tres historias tienen escenarios observables y prueba independiente.
- [x] CHK011 Se contemplan calendario, cambio de zona, suspensión, permisos, duplicados y fallos.
- [x] CHK012 La ventana, los avisos recuperados y los avisos antiguos están delimitados.
- [x] CHK013 La agenda base y la compatibilidad del navegador constan como dependencias.

## Preparación de la funcionalidad

- [x] CHK014 Los requisitos funcionales tienen escenarios o controles de validación asociados.
- [x] CHK015 Los escenarios cubren habilitación, emisión y prevención de avisos repetidos.
- [x] CHK016 Se define qué significa emitido sin equipararlo a leído o entrega garantizada.
- [x] CHK017 No quedan marcadores ni aclaraciones esenciales pendientes.

## Coherencia con la constitución y la agenda

- [x] CHK018 El alcance conserva el usuario único y no añade canales o configuraciones innecesarias.
- [x] CHK019 Se exige validación previa y pruebas automatizadas de límites, errores y regresión.
- [x] CHK020 La interfaz incluye teclado, lector de pantalla y adaptación a 360 y 1280 píxeles.

## Notas

- Decisiones confirmadas: notificación del navegador con la agenda abierta y
  horario fijo de 09:00 del día anterior, en zona local.
- Supuestos explícitos: recuperar durante el mismo día previo, omitir avisos viejos,
  no repetir una emisión confirmada y no reenviar automáticamente un resultado incierto.
- La comprobación de compatibilidad concreta y el diseño de persistencia y coordinación
  corresponden a la planificación; no se presume un soporte universal del navegador.
- La exclusión de recordatorios en la entrega 001 se conserva como límite histórico;
  esta especificación 002 define la extensión autorizada.
- La revisión documental no significa que exista implementación ni pruebas ejecutadas.
- Siguiente fase: `/speckit-plan` para esta funcionalidad.
