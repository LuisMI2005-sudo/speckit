# Plan de implementación: Organizador de tareas académicas de la UPB

**Rama**: `001-organizar-tareas-academicas` | **Fecha**: 2026-10-26
**Especificación**: [spec.md](spec.md)
**Entrada**: `specs/001-organizar-tareas-academicas/spec.md`
**Estado**: Diseño terminado; listo para descomponer en tareas.

## Resumen

Implementar una agenda académica local con materias y tareas, listado ordenado,
alertas temporales, completado y filtros combinados. Solo se borran materias vacías,
con confirmación y sin cascada. Un mismo proceso FastAPI sirve la interfaz y la API;
SQLite conserva la agenda entre reinicios. No hay cuentas ni sincronización.

## Contexto técnico

**Lenguaje y versión**: Python 3.12; HTML, CSS y JavaScript nativos.
**Dependencias principales**: FastAPI, Pydantic suministrado por FastAPI y Uvicorn.
**Almacenamiento**: SQLite mediante `sqlite3` estándar; `data/agenda.sqlite3` fuera
  del directorio servido. Ruta configurable con `UPB_DB_PATH`.
**Pruebas**: pytest, httpx/TestClient y pytest-playwright; ver [quickstart.md](quickstart.md).
**Plataforma objetivo**: Instancia local en computadora; interfaz de navegador
  adaptable a 360 y 1280 píxeles. Acceso local predeterminado por `127.0.0.1`.
**Tipo de proyecto**: Un único proyecto web, sin Docker ni microservicios.
**Objetivos de rendimiento**: Cinco materias y cien tareas; completar y filtrar
  en máximo un segundo en uso habitual; alertas actualizadas en máximo 60 segundos.
**Restricciones**: Una agenda por instalación y archivo de datos; sin autenticación,
  ORM, herramientas de compilación ni framework de frontend. Todo documento en español.
**Escala y alcance**: Un estudiante, dos entidades persistidas y las cinco historias
  de spec.md. No añadir edición, borrado de tareas ni reapertura de completadas.

## Comprobación de la constitución

| Control | Antes de investigación | Después del diseño | Evidencia prevista |
|---------|------------------------|--------------------|--------------------|
| Simplicidad y YAGNI | Cumple: pila y alcance acotados | Cumple: cuatro módulos y estáticos | Estructura y research.md |
| Pruebas obligatorias | Cumple: todos los flujos requieren pruebas | Cumple: matriz por historia y límites | Estrategia de pruebas y quickstart.md |
| Código legible | Cumple: responsabilidades separadas | Cumple: funciones pequeñas y nombres del dominio | Revisión de implementación y comentarios no obvios |
| Validación de entradas | Cumple: tabla de spec.md | Cumple: cliente, esquemas y restricciones de datos | data-model.md y contracts/api.md |
| Accesible y responsivo | Cumple: anchos y teclado definidos | Cumple: pruebas reales de navegador y revisión manual | contracts/interfaz.md |
| Documentos en español | Cumple | Cumple | Todos los artefactos de esta funcionalidad |

Los resultados indican conformidad del diseño; la entrega exige pruebas ejecutadas
con evidencia, revisión de código y comprobación manual. No hay excepciones.

## Estructura del proyecto

### Documentación de la funcionalidad

```text
specs/001-organizar-tareas-academicas/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── api.md
│   └── interfaz.md
└── checklists/requirements.md
```

`tasks.md` se generará mediante `/speckit-tasks`.

### Código fuente

Estructura prevista; estos archivos de aplicación aún no se crean en esta fase.

```text
app/
├── __init__.py
├── main.py           # Creación de app, rutas, respuesta HTML y errores
├── db.py             # Conexiones, esquema y consultas parametrizadas
├── schemas.py        # Esquemas y validadores de entrada
├── reglas.py         # Normalización y reglas de dominio del servidor
└── static/
    ├── index.html
    ├── styles.css
    └── app.js        # Formularios, consultas y funciones temporales puras
tests/
├── conftest.py       # SQLite temporal y servidor aislado para navegador
├── test_reglas.py
├── test_api.py
├── test_persistencia.py
└── test_interfaz.py
data/               # Archivo local ignorado por Git
requirements.txt
requirements-dev.txt
pytest.ini
.gitignore
```

**Decisión de estructura**: Un paquete y una carpeta de pruebas. Funciones directas
para consultas y rutas; no crear repositorios abstractos, servicios vacíos ni
proyectos separados. `reglas.py` permite probar normalización sin iniciar servidor.

## Diseño de comportamiento

- Usar una fábrica `crear_app(ruta_db)` para aislar pruebas; exponer `app` desde
  main.py para Uvicorn. Inicializar esquema en el ciclo de vida, sin borrar datos.
- Abrir/cerrar conexiones dentro de cada operación síncrona de base de datos;
  confirmar todo cambio o revertirlo. Activar claves foráneas antes de transacciones.
- SQLite es la fuente de verdad. No persistir una segunda agenda en el navegador.
  Todos los perfiles de esa instancia ven la misma agenda.
- Validar tipos estrictos, límites, fechas, colores y claves de materia en servidor;
  replicar validaciones de formulario para respuesta inmediata. Traducir errores
  de Pydantic y base de datos al formato en español del contrato.
- El servidor devuelve fecha y estado; JavaScript deriva la alerta con el reloj
  del dispositivo. Una tarea completada nunca recibe alerta temporal.
- Servir estáticos solo desde `app/static/`. Mostrar texto con `textContent`, nunca
  interpolar contenido de usuario como HTML. Usar SQL con parámetros.
- Mantener origen único y peticiones JSON. No habilitar acceso público ni CORS
  amplio. Registrar fallos operativos sin volcar descripciones o consultas con datos.

## Estrategia de pruebas y entrega

| Cobertura | Pruebas previstas |
|-----------|-------------------|
| Historia 1, FR-002/003/017 | Alta, NFC, duplicados, paleta, borrar vacía, cancelar, bloqueo con pendientes y completadas, filtro activo |
| Historia 2, FR-004/005/013 | Alta con/sin descripción, materia ausente, fecha imposible/pasada, errores sin guardado parcial |
| Historia 3, FR-006/007/015 | Orden por fecha/id, reloj controlado, 48 h ±1 ms, vencimiento ±1 ms, fin de mes/año, horario estacional |
| Historia 4, FR-008 | Completado idempotente, conservación de datos y ausencia de alertas |
| Historia 5, FR-009/010/011 | Filtros individuales/combinados, vacíos, restablecimiento y resultados ordenados |
| FR-001/012/014 | Sin login, agenda compartida por instancia, reiniciar contra mismo archivo, errores en español |
| Límites | Materia 0/1/100/101, título 0/1/150/151, descripción 0/2000/2001; emoji y acentos combinados |
| Integridad | Claves foráneas en cada conexión, borrar/crear concurrentes, rollback y bloqueo temporal |
| UI-001 a UI-005 | Flujos a 360/1280, teclado, foco, etiquetas, errores asociados, avisos y texto de alertas |

Usar SQLite temporal por prueba. Las pruebas de persistencia crean una segunda app
contra el mismo archivo. Las de navegador arrancan un servidor efímero aislado y
lo cierran al terminar; no usar datos reales. pytest-playwright se utiliza solo en
desarrollo. El reloj del navegador se controla sin esperas reales de 48 horas.

La implementación debe ejecutar `python -m pytest`, documentar comando/resultados
y verificar manualmente teclado, legibilidad y lector de pantalla. SC-001 requiere
además evaluación con cinco estudiantes; no se sustituye por una prueba sintética.
SC-002 a SC-009 se verifican con los datos y escenarios definidos en spec.md.

## Seguimiento de complejidad

No hay violaciones ni complejidad adicional que justificar. La herramienta de
navegador es necesaria para probar el JavaScript y la adaptación exigidos por la
constitución; no añade dependencias al producto frontend.

## Secuencia de trabajo prevista

1. Preparar aplicación, esquema, validadores y pruebas aisladas.
2. Entregar materias y tareas con persistencia y pruebas de integración.
3. Incorporar listado, alertas, completado y filtros con pruebas de navegador.
4. Verificar borrado protegido, accesibilidad, errores y regresiones completas.
5. Registrar resultados y evaluación de éxito antes de dar por terminada la entrega.

Siguiente comando: `/speckit-tasks`. Este plan no ejecuta la implementación.
