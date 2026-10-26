# Plan de implementación: Recordatorios de tareas

**Rama**: `002-agregar-recordatorios-tareas` | **Fecha**: 2026-10-26
**Especificación**: [spec.md](spec.md)

## Resumen

Implementar la agenda base indispensable y sus recordatorios locales. Una página
servida por FastAPI solicita permiso tras una acción explícita y evalúa cada 30
segundos. SQLite coordina reservas entre pestañas y perfiles. Solo se emite para
pendientes, entre las 09:00 del día anterior y las 00:00 del día de entrega.

## Contexto técnico

- Lenguaje: Python 3.12; HTML/CSS/JavaScript sin frameworks.
- Dependencias: FastAPI, Uvicorn y tzdata para zonas IANA en Windows; sqlite3 estándar.
- Pruebas: pytest, httpx y pytest-playwright con Chromium, archivo temporal y reloj controlado.
- Plataforma: instancia local en computadora; navegador compatible en entorno seguro.
  localhost permite desarrollo; acceder desde teléfono exige HTTPS y soporte de
  notificaciones. Si faltan capacidades, la agenda sigue disponible con explicación.
- Tipo: un solo proyecto, sin ORM, Docker, servicios externos ni proceso de programación separado.
- Alcance: agenda por instalación, cinco materias/cien tareas de referencia;
  veinte tareas para evaluar recordatorios; ventana de actualización máxima de 60 s.
- Notificaciones: service worker registrado por la página y showNotification;
  sin eventos push ni programación en segundo plano con la agenda cerrada.

## Comprobación de la constitución

| Principio | Antes de investigar | Después de diseñar |
|-----------|--------------------|--------------------|
| Simplicidad | Cumple: pila acordada | Cumple: un proceso y SQL directo |
| Pruebas obligatorias | Requeridas por historia | Pruebas API, calendario, carrera y navegador previstas |
| Código legible | Funciones pequeñas | Módulos de reglas, datos y transporte |
| Validación | No confiar en datos del cliente | Fechas, zonas, identidades, tokens y resultados estrictos |
| Accesibilidad y adaptación | 360/1280 y teclado | Formularios semánticos, foco y avisos textuales |
| Español | Documentación en español | Mensajes y evidencias en español |

Estos controles validan el diseño; las tareas de cierre requieren ejecución real.

## Estructura del proyecto

### Documentación de la funcionalidad

spec.md, plan.md, research.md, data-model.md, contracts/api.md, quickstart.md,
tasks.md y evidencias.md dentro de esta carpeta.

### Código fuente

```text
app/
  __init__.py
  main.py                 # Aplicación y validación de contratos
  reglas.py               # Normalización y ventana local
  db.py                   # Transacciones y reservas
  static/
    index.html
    styles.css
    app.js                # Agenda y filtros
    recordatorios.js      # Permisos y coordinación de emisión
    sw.js                 # Soporte de notificaciones del navegador
 tests/
  conftest.py
  test_api.py
  test_reglas.py
  test_recordatorios.py
  test_interfaz.py
 requirements.txt
 requirements-dev.txt
 pytest.ini
```

Usar rutas relativas al proyecto; ignorar .venv/, .runtime/, data/ y cachés.

## Diseño y decisiones

La dependencia 001 no tiene código: implementar materias, tareas, completado,
filtros, urgencia y persistencia como fundamento necesario de FR-012 de 002;
no dar por ejecutadas ni reescribir las tareas históricas de 001.

El navegador comunica instante ISO con zona y zona IANA actual; el servidor convierte
ese instante para validar la ventana. No depende de la zona del servidor. Una
reserva atómica deja resultado incierto y token aleatorio; solo un cliente gana.
Antes de emitir, autorizar una sola vez el token comprobando tarea y ventana.
Confirmar emitido tras aceptación del navegador; fracaso conocido vuelve a no_emitido;
una caída deja incierto sin caducidad ni reenvío. Confirmaciones repetidas son
idempotentes. Completar después de autorizar no puede deshacer una emisión autorizada.

Validar todas las entradas, traducir errores, SQL parametrizado y texto literal.
Los controles de permisos no disparan diálogos automáticamente. Service worker
sin caché ni emisión autónoma. Se prueban registro real y permisos; las pruebas de
entrega sustituyen únicamente la frontera del SO, sin afirmar lectura humana.

## Estrategia de pruebas

Pruebas puras de normalización/calendario y pruebas de API con SQLite temporal,
concurrencia, idempotencia, rollback y reinicio. Navegador real a 360/1280 con
service worker activado y entrega controlada: permisos, veinte tareas, límites,
diez reevaluaciones, recarga, dos contextos, fallos y tarea completada. Revisar
manualmente teclado, foco y disposición mediante navegador. Registrar comandos,
resultados y límites de comprobación visual del sistema operativo en evidencias.md.

## Seguimiento de complejidad

La tabla de reservas y el service worker son necesarios para deduplicar entre
perfiles y admitir la vía de notificaciones móvil. No se introduce infraestructura
adicional. No hay excepciones a la constitución ni decisiones esenciales pendientes.
