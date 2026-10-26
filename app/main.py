"""Contratos y aplicación del único proyecto local."""
import logging
import os
import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from fastapi import FastAPI, Query, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr, field_validator
from starlette.exceptions import HTTPException
from . import db
from .reglas import COLORES, fecha_valida, normalizar_texto

ESTATICOS = Path(__file__).parent / 'static'

class Entrada(BaseModel):
    model_config = ConfigDict(extra='forbid')

class MateriaEntrada(Entrada):
    nombre: StrictStr
    color: Literal['azul','verde','rojo','naranja','morado','turquesa']
    @field_validator('nombre')
    @classmethod
    def nombre_valido(cls, valor):
        return normalizar_texto(valor,100)

class TareaEntrada(Entrada):
    materia_id: StrictInt
    titulo: StrictStr
    descripcion: StrictStr | None = ''
    fecha_entrega: StrictStr
    @field_validator('materia_id')
    @classmethod
    def identidad_positiva(cls,valor):
        if valor <= 0: raise ValueError('Selecciona una materia existente')
        return valor
    @field_validator('titulo')
    @classmethod
    def titulo_valido(cls,valor): return normalizar_texto(valor,150)
    @field_validator('descripcion')
    @classmethod
    def descripcion_valida(cls,valor): return normalizar_texto(valor or '',2000,True)
    @field_validator('fecha_entrega')
    @classmethod
    def fecha(cls,valor): return fecha_valida(valor)

class Contexto(Entrada):
    ahora: datetime
    zona: StrictStr
    @field_validator('ahora', mode='before')
    @classmethod
    def instante(cls,valor):
        if not isinstance(valor,str): raise ValueError('Usa un instante ISO con zona horaria')
        dato=datetime.fromisoformat(valor.replace('Z','+00:00'))
        if dato.tzinfo is None: raise ValueError('La hora requiere zona horaria')
        return dato
    @field_validator('zona')
    @classmethod
    def zona_valida(cls,valor):
        try: ZoneInfo(valor)
        except (ZoneInfoNotFoundError,ValueError): raise ValueError('Zona horaria no válida')
        return valor

class Resultado(Entrada):
    resultado: Literal['emitido','no_emitido']

def error(estado,codigo,mensaje,campos=None):
    return JSONResponse(status_code=estado,content={'error':{'codigo':codigo,'mensaje':mensaje,'campos':campos or {}}})

def crear_app(ruta_db=None):
    ruta = Path(ruta_db or os.environ.get('UPB_DB_PATH',Path(__file__).parent.parent/'data'/'agenda.sqlite3'))
    @asynccontextmanager
    async def vida(app):
        try: db.inicializar(ruta)
        except (sqlite3.Error,OSError):
            logging.getLogger(__name__).error('No se pudo inicializar el almacenamiento')
        yield
    app = FastAPI(title='Agenda académica UPB',lifespan=vida,docs_url=None,redoc_url=None)
    app.state.ruta_db = ruta
    app.mount('/static',StaticFiles(directory=ESTATICOS),name='static')

    @app.exception_handler(RequestValidationError)
    async def validacion(request,exc):
        campos={str(e['loc'][-1]):'Dato no válido o fuera de los límites permitidos' for e in exc.errors()}
        return error(422,'validacion','Revisa los datos ingresados',campos)
    @app.exception_handler(db.ErrorDominio)
    async def dominio(request,exc):
        return error(exc.estado,exc.codigo,exc.mensaje,exc.campos)
    @app.exception_handler(sqlite3.IntegrityError)
    async def integridad(request,exc):
        return error(409,'conflicto','Los datos están en conflicto; revisa la agenda')
    @app.exception_handler(sqlite3.Error)
    async def almacenamiento(request,exc):
        return error(503,'almacenamiento_no_disponible','No se pudieron guardar o recuperar los datos. Intenta de nuevo')
    @app.exception_handler(HTTPException)
    async def http_error(request,exc):
        return error(exc.status_code,'no_encontrado' if exc.status_code==404 else 'peticion_invalida','El recurso no está disponible')
    @app.exception_handler(Exception)
    async def inesperado(request,exc):
        logging.getLogger(__name__).error('Error inesperado de aplicación')
        return error(500,'error_interno','Ocurrió un error inesperado')

    @app.get('/')
    def inicio(): return FileResponse(ESTATICOS/'index.html')
    @app.get('/sw.js')
    def service_worker(): return FileResponse(ESTATICOS/'sw.js',media_type='application/javascript',headers={'Cache-Control':'no-cache'})
    @app.get('/api/materias')
    def materias():
        with db.conectar(ruta) as con:
            return [dict(f) for f in con.execute('SELECT id,nombre,color FROM materias ORDER BY id')]
    @app.post('/api/materias',status_code=201)
    def crear_materia(dato:MateriaEntrada):
        with db.conectar(ruta,True) as con:
            try:
                cursor=con.execute('INSERT INTO materias(nombre,nombre_clave,color) VALUES (?,?,?)',(dato.nombre,dato.nombre.casefold(),dato.color))
            except sqlite3.IntegrityError:
                raise db.ErrorDominio(409,'materia_duplicada','Esta materia ya existe',{'nombre':'Esta materia ya existe'})
            return {'id':cursor.lastrowid,'nombre':dato.nombre,'color':dato.color}
    @app.delete('/api/materias/{identidad}',status_code=204)
    def borrar_materia(identidad:int):
        with db.conectar(ruta,True) as con:
            db.existente(con,'materias',identidad)
            if con.execute('SELECT 1 FROM tareas WHERE materia_id=?',(identidad,)).fetchone():
                raise db.ErrorDominio(409,'materia_con_tareas','No puedes borrar una materia con tareas')
            con.execute('DELETE FROM materias WHERE id=?',(identidad,))
        return Response(status_code=204)
    @app.post('/api/tareas',status_code=201)
    def crear_tarea(dato:TareaEntrada):
        with db.conectar(ruta,True) as con:
            if con.execute('SELECT 1 FROM materias WHERE id=?',(dato.materia_id,)).fetchone() is None:
                raise db.ErrorDominio(422,'validacion','Selecciona una materia existente',{'materia_id':'Selecciona una materia existente'})
            cursor=con.execute('INSERT INTO tareas(materia_id,titulo,descripcion,fecha_entrega) VALUES (?,?,?,?)',(dato.materia_id,dato.titulo,dato.descripcion or '',dato.fecha_entrega))
            return db.existente(con,'tareas',cursor.lastrowid)
    @app.get('/api/tareas')
    def tareas(materia_id:int|None=Query(None,gt=0),estado:Literal['pendiente','completada']|None=None):
        with db.conectar(ruta) as con:
            if materia_id is not None and con.execute('SELECT 1 FROM materias WHERE id=?',(materia_id,)).fetchone() is None:
                raise db.ErrorDominio(422,'validacion','Selecciona una materia existente')
            return [dict(f) for f in con.execute('SELECT * FROM tareas WHERE (? IS NULL OR materia_id=?) AND (? IS NULL OR estado=?) ORDER BY fecha_entrega,id',(materia_id,materia_id,estado,estado))]
    @app.patch('/api/tareas/{identidad}/completar')
    def completar(identidad:int):
        with db.conectar(ruta,True) as con:
            db.existente(con,'tareas',identidad)
            con.execute("UPDATE tareas SET estado='completada' WHERE id=?",(identidad,))
            return db.existente(con,'tareas',identidad)
    @app.get('/api/recordatorios')
    def estados():
        with db.conectar(ruta) as con:
            return [dict(f) for f in con.execute('SELECT tarea_id,fecha_entrega,resultado FROM recordatorios ORDER BY tarea_id')]
    @app.post('/api/recordatorios/reservar')
    def reservar(contexto:Contexto):
        with db.conectar(ruta,True) as con: return db.reservar(con,contexto)
    @app.post('/api/recordatorios/{token}/autorizar')
    def autorizar(token:str,contexto:Contexto):
        with db.conectar(ruta,True) as con: return db.autorizar(con,token,contexto)
    @app.post('/api/recordatorios/{token}/resultado')
    def confirmar(token:str,dato:Resultado):
        with db.conectar(ruta,True) as con: return db.confirmar(con,token,dato.resultado)
    return app

app = crear_app()
