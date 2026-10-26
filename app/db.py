"""SQLite local con transacciones breves y reservas entre clientes."""
import sqlite3
import uuid
from contextlib import contextmanager
from pathlib import Path
from .reglas import ventana_recordatorio

ESQUEMA = """
CREATE TABLE IF NOT EXISTS materias (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nombre TEXT NOT NULL CHECK(length(nombre) BETWEEN 1 AND 100),
 nombre_clave TEXT NOT NULL UNIQUE,
 color TEXT NOT NULL CHECK(color IN ('azul','verde','rojo','naranja','morado','turquesa'))
);
CREATE TABLE IF NOT EXISTS tareas (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 materia_id INTEGER NOT NULL REFERENCES materias(id) ON DELETE RESTRICT,
 titulo TEXT NOT NULL CHECK(length(titulo) BETWEEN 1 AND 150),
 descripcion TEXT NOT NULL DEFAULT '' CHECK(length(descripcion)<=2000),
 fecha_entrega TEXT NOT NULL,
 estado TEXT NOT NULL DEFAULT 'pendiente' CHECK(estado IN ('pendiente','completada'))
);
CREATE INDEX IF NOT EXISTS tareas_materia ON tareas(materia_id);
CREATE TABLE IF NOT EXISTS recordatorios (
 tarea_id INTEGER NOT NULL REFERENCES tareas(id) ON DELETE RESTRICT,
 fecha_entrega TEXT NOT NULL,
 resultado TEXT NOT NULL CHECK(resultado IN ('no_emitido','incierto','emitido')),
 token TEXT NOT NULL UNIQUE,
 autorizado INTEGER NOT NULL DEFAULT 0 CHECK(autorizado IN (0,1)),
 PRIMARY KEY(tarea_id,fecha_entrega)
);
"""

class ErrorDominio(Exception):
    def __init__(self, estado, codigo, mensaje, campos=None):
        self.estado, self.codigo, self.mensaje = estado, codigo, mensaje
        self.campos = campos or {}

@contextmanager
def conectar(ruta, escritura=False):
    con = sqlite3.connect(ruta, timeout=5, autocommit=True)
    con.row_factory = sqlite3.Row
    try:
        con.execute('PRAGMA foreign_keys=ON')
        if escritura:
            con.execute('BEGIN IMMEDIATE')
        yield con
        if con.in_transaction:
            con.execute('COMMIT')
    except BaseException:
        if con.in_transaction:
            con.execute('ROLLBACK')
        raise
    finally:
        con.close()

def inicializar(ruta):
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    with conectar(ruta) as con:
        con.executescript(ESQUEMA)

def existente(con, tabla, identidad):
    # Los nombres de tabla son constantes internas, nunca datos del usuario.
    fila = con.execute(f'SELECT * FROM {tabla} WHERE id=?', (identidad,)).fetchone()
    if fila is None:
        raise ErrorDominio(404, 'no_encontrado', 'La materia o tarea no existe')
    return dict(fila)

def reservar(con, contexto):
    pendientes = con.execute("SELECT t.*,m.nombre AS materia FROM tareas t JOIN materias m ON m.id=t.materia_id WHERE t.estado='pendiente'").fetchall()
    resultado = []
    for fila in pendientes:
        if not ventana_recordatorio(fila['fecha_entrega'], contexto.ahora, contexto.zona):
            continue
        previo = con.execute('SELECT resultado FROM recordatorios WHERE tarea_id=? AND fecha_entrega=?', (fila['id'], fila['fecha_entrega'])).fetchone()
        if previo and previo['resultado'] != 'no_emitido':
            continue
        token = str(uuid.uuid4())
        con.execute("INSERT INTO recordatorios(tarea_id,fecha_entrega,resultado,token,autorizado) VALUES (?,?,'incierto',?,0) ON CONFLICT(tarea_id,fecha_entrega) DO UPDATE SET resultado='incierto',token=excluded.token,autorizado=0", (fila['id'], fila['fecha_entrega'], token))
        resultado.append({'token':token, 'tarea_id':fila['id'], 'titulo':fila['titulo'], 'materia':fila['materia'], 'fecha_entrega':fila['fecha_entrega']})
    return resultado

def registro_token(con, token):
    fila = con.execute('SELECT * FROM recordatorios WHERE token=?',(token,)).fetchone()
    if fila is None:
        raise ErrorDominio(404,'no_encontrado','El recordatorio no existe')
    return dict(fila)

def autorizar(con, token, contexto):
    registro = registro_token(con, token)
    tarea = existente(con, 'tareas', registro['tarea_id'])
    if registro['autorizado'] or registro['resultado'] != 'incierto' or tarea['estado'] != 'pendiente' or tarea['fecha_entrega'] != registro['fecha_entrega'] or not ventana_recordatorio(tarea['fecha_entrega'],contexto.ahora,contexto.zona):
        raise ErrorDominio(409,'no_elegible','El recordatorio ya no puede emitirse')
    con.execute('UPDATE recordatorios SET autorizado=1 WHERE token=?',(token,))
    materia = existente(con,'materias',tarea['materia_id'])
    return {'tarea_id':tarea['id'],'titulo':tarea['titulo'],'materia':materia['nombre'],'fecha_entrega':tarea['fecha_entrega']}

def confirmar(con, token, resultado):
    registro = registro_token(con,token)
    if not registro['autorizado']:
        raise ErrorDominio(409,'sin_autorizacion','No se autorizó esta emisión')
    if registro['resultado'] not in ('incierto',resultado):
        raise ErrorDominio(409,'resultado_contradictorio','El resultado ya fue confirmado')
    con.execute('UPDATE recordatorios SET resultado=? WHERE token=?',(resultado,token))
    return {'resultado':resultado}
