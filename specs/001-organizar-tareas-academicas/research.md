# Investigación: Organizador de tareas académicas

**Fecha**: 2026-10-26
**Estado**: Decisiones resueltas para planificación; no implica implementación.

## Aplicación y persistencia

**Decisión**: Un proceso local de FastAPI con Python 3.12, archivos HTML/CSS/JS y
SQLite mediante `sqlite3`. Servir `/` con el documento principal y `/static/` con
`StaticFiles`. Usar operaciones síncronas para SQLite y SQL parametrizado.
**Motivo**: Cumple la pila solicitada con un único origen y pocas dependencias.
**Alternativas**: ORM, servidor independiente de interfaz, Docker y microservicios
no aportan valor al alcance actual. No se incorporan.
**Fuentes**: [Archivos estáticos de FastAPI](https://fastapi.tiangolo.com/tutorial/static-files/)
y [sqlite3 en Python 3.12](https://docs.python.org/3.12/library/sqlite3.html).

## Unidad de usuario y despliegue

**Decisión**: Una agenda por archivo SQLite e instalación, accesible en la instancia
local de FastAPI. Escuchar en `127.0.0.1` de forma predeterminada. No crear cuentas.
**Motivo**: La persistencia solicitada reside en el servidor local; distintos perfiles
que accedan a él comparten datos. Se actualizó el supuesto anterior por navegador.
**Alternativas**: Una instalación pública compartida o agendas separadas por cookies
necesitarían identidad y aislamiento fuera del alcance. El diseño responsivo se
valida en navegador a tamaños de celular y computadora; no se presupone que Python
se ejecute en un teléfono ni se publica el servicio en Internet.

## Integridad y borrado

**Decisión**: `FOREIGN KEY ... ON DELETE RESTRICT` y `PRAGMA foreign_keys=ON` en cada
conexión antes de iniciar transacciones. Borrar solo materias sin tareas, tras
confirmación; cualquier estado de tarea bloquea el borrado con conflicto.
**Motivo**: Preserva también tareas completadas y protege frente a carreras.
**Alternativas**: Cascada u orfandad contradicen la respuesta del usuario.
**Fuente**: [Claves foráneas de SQLite](https://www.sqlite.org/foreignkeys.html).

Abrir conexión por operación completa, activar/verificar claves foráneas con
`autocommit=True`, cambiar después a `autocommit=False`, ejecutar la operación y
confirmar o revertir explícitamente; cerrar siempre en `finally`. No compartir una
conexión global entre hilos. El contexto de conexión no sustituye su cierre.
Traducir conflictos de integridad y bloqueos temporales a errores en español.

## Texto y validación

**Decisión**: Normalización NFC, recorte exterior de nombre/título y conteo por
puntos de código: `len()` en Python y `Array.from(texto.normalize('NFC')).length`
en JavaScript. Límites confirmados: 100, 150 y 2000. No truncar.
**Motivo**: Evita discrepancias entre bytes, UTF-16 y caracteres normalizados.
**Alternativas**: Solo `maxlength` o límites solo en interfaz no garantizan igualdad.
La unicidad usa una clave `casefold()` del nombre normalizado, con restricción UNIQUE;
no confiar en `NOCASE` de SQLite para toda la comparación Unicode.
**Fuentes**: [Normalización de cadenas](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/normalize)
y [Longitud de cadenas](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/length).

## Cálculo de urgencia

**Decisión**: Guardar fecha de calendario sin hora; calcular la alerta en JavaScript
con reloj y zona local del navegador. Crear la medianoche local del día siguiente
por componentes de calendario; evitar interpretar la cadena de fecha como UTC y
sumar 24 horas a la fecha. Restar los instantes resultantes en milisegundos.
**Motivo**: Respeta fin de día y cambios de horario; 48 horas son 172800000 ms reales.
**Alternativas**: Dos días de calendario o reloj del servidor contradicen la regla
confirmada. No se almacena una alerta que pueda quedar obsoleta.
Actualizar cada 30 segundos y en `focus`/`visibilitychange`; recalcular antes de
presentar una vista recuperada. Inyectar el instante en la función para pruebas.
**Fuente**: [Fechas y avance de calendario local](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/setDate).

## Pruebas

**Decisión**: pytest, `TestClient`/httpx para API y SQLite temporal; pytest-playwright
para ejecutar la interfaz real y comprobar anchos, Unicode, filtros y reloj.
**Motivo**: Las pruebas de servidor solas no comprueban el comportamiento del JavaScript.
**Alternativas**: Solo revisión manual incumple la constitución; una herramienta de
navegador en desarrollo no introduce un framework en la interfaz del producto.
**Fuentes**: [Pruebas de FastAPI](https://fastapi.tiangolo.com/tutorial/testing/)
y [Playwright con pytest](https://playwright.dev/python/docs/intro).

No quedan decisiones técnicas pendientes. Las versiones exactas de dependencias
se resolverán con Python 3.12 durante la implementación y se guardarán en archivos
de requisitos reproducibles tras verificar compatibilidad; no se afirma una
instalación o ejecución de pruebas que todavía no ocurrió.
