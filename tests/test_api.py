"""Contratos de la agenda base y conservación de datos."""
import sqlite3
import pytest
from fastapi.testclient import TestClient
from app.main import crear_app

@pytest.mark.parametrize('nombre,color', [('', 'azul'), (' '*3, 'azul'), ('a'*101, 'azul'), ('válida', 'negro')])
def test_materia_invalida(cliente, nombre, color):
    r=cliente.post('/api/materias', json={'nombre':nombre, 'color':color})
    assert r.status_code == 422
    assert 'error' in r.json()
    assert cliente.get('/api/materias').json() == []

def test_materias_duplicados_y_borrado(cliente, materia, tarea):
    assert cliente.post('/api/materias', json={'nombre':' cálculo i ', 'color':'rojo'}).status_code==409
    assert cliente.post('/api/materias', json={'nombre':'Calculo I', 'color':'azul'}).status_code==201
    dato=tarea(estado='completada')
    assert cliente.delete(f"/api/materias/{materia['id']}").status_code==409
    assert len(cliente.get('/api/tareas').json())==1
    vacia=cliente.post('/api/materias', json={'nombre':'Historia', 'color':'verde'}).json()
    assert cliente.delete(f"/api/materias/{vacia['id']}").status_code==204
    assert cliente.delete('/api/materias/999').status_code==404

@pytest.mark.parametrize('cambio', [
    {'titulo':''}, {'titulo':'x'*151}, {'descripcion':'x'*2001},
    {'fecha_entrega':'2026-02-30'}, {'fecha_entrega':'2026-01-01T00:00:00'},
    {'materia_id':True}, {'materia_id':999}, {'estado':'completada'}, {'titulo':'x\x00y'}])
def test_tarea_invalida(cliente, materia, cambio):
    datos={'materia_id':materia['id'], 'titulo':'Tarea', 'fecha_entrega':'2026-10-28'} | cambio
    assert cliente.post('/api/tareas', json=datos).status_code==422
    assert cliente.get('/api/tareas').json()==[]

def test_limites_y_filtros(cliente, materia, tarea):
    dato=tarea(fecha='2020-01-01', titulo='😀'*150)
    r=cliente.post('/api/tareas', json={'materia_id':materia['id'],'titulo':'Otra','descripcion':'é'*2000,'fecha_entrega':'2026-12-01'})
    assert r.status_code==201
    assert cliente.patch(f"/api/tareas/{dato['id']}/completar").json()['estado']=='completada'
    assert cliente.patch(f"/api/tareas/{dato['id']}/completar").status_code==200
    pendientes=cliente.get('/api/tareas',params={'estado':'pendiente','materia_id':materia['id']}).json()
    assert len(pendientes)==1
    assert pendientes[0]['titulo']=='Otra'
    assert cliente.get('/api/tareas?estado=extraño').status_code==422
    assert cliente.get('/api/tareas?materia_id=999').status_code==422

def test_persistencia_y_fk(cliente, archivo, materia, tarea):
    tarea()
    with TestClient(crear_app(archivo)) as otro:
        assert otro.get('/api/materias').json()==[materia]
        assert len(otro.get('/api/tareas').json())==1
    with sqlite3.connect(archivo) as con:
        con.execute('PRAGMA foreign_keys=ON')
        with pytest.raises(sqlite3.IntegrityError):
            con.execute('DELETE FROM materias WHERE id=?',(materia['id'],))
    assert cliente.get('/static/../data/agenda.sqlite3').status_code==404
    assert cliente.get('/').status_code==200
    assert cliente.get('/sw.js').status_code==200

def test_fallo_archivo_no_se_sustituye(tmp_path):
    archivo=tmp_path/'corrupto.sqlite3'
    archivo.write_bytes(b'no soy sqlite')
    with TestClient(crear_app(archivo), raise_server_exceptions=False) as cliente:
        assert cliente.get('/api/materias').status_code==503
    assert archivo.read_bytes()==b'no soy sqlite'
