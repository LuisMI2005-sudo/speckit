# Ejecución y validación

Desde la raíz del proyecto, en PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abrir http://127.0.0.1:8000, registrar materia y tarea con entrega mañana y activar
recordatorios. Se recuperan desde las 09:00 hasta el inicio del día de entrega.
La fecha y hora local del dispositivo son la referencia. No cambiar el reloj real
para probar: las pruebas inyectan contexto temporal.

Si Python 3.12 no está instalado, se puede usar uv python install 3.12 y crear el
entorno con uv venv --python 3.12 .venv. El archivo data/agenda.sqlite3 persiste;
UPB_DB_PATH selecciona otro archivo y las pruebas siempre usan uno temporal.

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Se necesita Chromium para pruebas de navegador. No se usa la agenda real.
localhost es el entorno de desarrollo; uso desde un teléfono requiere acceso
HTTPS y navegador compatible. Permisos denegados o capacidad ausente muestran
explicación sin bloquear el resto de la agenda. No hay promesa de entrega si la
página está cerrada o suspendida. La prueba controlada de showNotification no
certifica la presentación del sistema operativo ni la lectura del estudiante.
