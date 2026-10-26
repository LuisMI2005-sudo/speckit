# Guía de ejecución y pruebas

**Estado**: Procedimiento previsto para la implementación. Los archivos de código,
requisitos y pruebas indicados se crearán después de `/speckit-tasks`; esta fase
solo genera documentación y no afirma que esos comandos ya hayan pasado.

## Requisitos

Python 3.12 instalado y una terminal situada en la raíz del proyecto. Un navegador
para uso manual. Las pruebas de interfaz instalarán Chromium mediante Playwright;
no se necesita Node ni compilación del frontend.

## Preparación en Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

`requirements.txt` contendrá FastAPI y Uvicorn, con dependencias resueltas para
Python 3.12. `requirements-dev.txt` incluirá el archivo anterior, pytest, httpx y
pytest-playwright. Guardar versiones exactas verificadas al implementar; sqlite3
forma parte de Python y no se instala por pip.

## Inicio local

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abrir [la agenda local](http://127.0.0.1:8000/). El mismo FastAPI sirve HTML, CSS,
JavaScript y API. Por defecto se usa `data/agenda.sqlite3`, fuera de los estáticos.
Para una instalación separada, antes de iniciar:

```powershell
$env:UPB_DB_PATH = Join-Path (Get-Location) 'data\otra-agenda.sqlite3'
```

Las pruebas siempre usarán una ruta temporal explícita y no modificarán esa agenda.
Cerrar el navegador o reiniciar FastAPI conserva el archivo. Acceder desde otro
perfil al mismo proceso comparte los datos. El servicio local debe estar en marcha
para leer o guardar; no se ofrece funcionamiento sin servidor ni sincronización.
La adaptación a celular se valida por tamaños de navegador, sin exponer la agenda
local a una red pública.

## Ejecución automatizada

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_reglas.py tests/test_api.py tests/test_persistencia.py
.\.venv\Scripts\python.exe -m pytest tests/test_interfaz.py --browser chromium
.\.venv\Scripts\python.exe -m pytest
```

`conftest.py` deberá proporcionar un archivo SQLite temporal y arrancar/cerrar el
servidor para las pruebas de navegador, sin pasos manuales paralelos. Parametrizar
las vistas a 360 y 1280 píxeles. Los tres comandos deben finalizar sin errores;
registrar fecha, comando, cantidad de pruebas y resultado en la evidencia de entrega.
No interpretar la ausencia de pruebas como éxito.

## Comprobación manual complementaria

1. Crear una materia con nombre/color y tareas con y sin descripción.
2. Comprobar el orden, materia y estado; revisar una fecha pasada y otra cercana.
3. Completar una tarea y filtrar por materia/estado, incluido cero coincidencias.
4. Confirmar que una materia con tareas no se borra, aunque todas estén completadas.
5. Crear una materia vacía; cancelar primero y luego confirmar su borrado.
6. Probar longitudes máximas, excesos, espacios y textos con tildes/emoji; verificar
   mensajes asociados a campos y que no haya truncamiento ni pérdida del formulario.
7. Repetir los flujos con teclado y lector de pantalla; revisar foco, avisos y
   presentación a 360 y 1280 píxeles.
8. Reiniciar FastAPI usando el mismo archivo y comprobar que los datos continúan.
9. Realizar la evaluación de SC-001 con cinco estudiantes y registrar tiempos.

Las fronteras de urgencia se prueban con reloj controlado en pruebas automatizadas;
no se requiere esperar 48 horas ni cambiar el reloj real del dispositivo.

## Manejo de fallos

Si un guardado falla, mantener los campos y reintentar solo tras revisar el mensaje;
no afirmar que quedó guardado. Si SQLite no puede abrirse o recuperarse, revisar la
ruta y permisos sin sustituir el archivo por otro vacío. Detener el servidor con
Ctrl+C al terminar. No borrar el archivo de datos para solucionar un fallo.
