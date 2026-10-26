"""Reservas compartidas, fallos e idempotencia sin promesas de lectura del SO."""
from concurrent.futures import ThreadPoolExecutor
import pytest
from fastapi.testclient import TestClient
from app.main import crear_app

CONTEXTO={'ahora':'2026-10-27T15:00:00-04:00','zona':'America/La_Paz'}

def reservar(cliente, contexto=None):
    r=cliente.post('/api/recordatorios/reservar',json=contexto or CONTEXTO)
    assert r.status_code==200, r.text
    return r.json()

def autorizar(cliente, token, contexto=None):
    return cliente.post(f'/api/recordatorios/{token}/autorizar',json=contexto or CONTEXTO)

def resultado(cliente, token, valor='emitido'):
    return cliente.post(f'/api/recordatorios/{token}/resultado',json={'resultado':valor})

def test_veinte_y_no_elegibles(cliente, tarea):
    for _ in range(20): tarea()
    tarea(estado='completada'); tarea(fecha='2026-10-27'); tarea(fecha='2026-10-29')
    assert reservar(cliente,CONTEXTO | {'ahora':'2026-10-27T08:59:59-04:00'})==[]
    reservas=reservar(cliente)
    assert len(reservas)==20
    assert all('descripcion' not in dato for dato in reservas)
    for _ in range(10): assert reservar(cliente)==[]
    for dato in reservas:
        assert autorizar(cliente,dato['token']).status_code==200
        assert resultado(cliente,dato['token']).status_code==200
    assert all(d['resultado']=='emitido' for d in cliente.get('/api/recordatorios').json())

def test_dos_clientes_compiten(cliente, tarea, archivo):
    tarea()
    def intento(_):
        with TestClient(crear_app(archivo)) as otro: return reservar(otro)
    with ThreadPoolExecutor(max_workers=2) as ejecutor:
        resultados=list(ejecutor.map(intento,range(2)))
    assert sum(len(r) for r in resultados)==1

def test_completar_antes_autorizar(cliente,tarea):
    dato=tarea(); token=reservar(cliente)[0]['token']
    cliente.patch(f"/api/tareas/{dato['id']}/completar")
    assert autorizar(cliente,token).status_code==409
    assert reservar(cliente)==[]

def test_idempotencia_y_error_conocido(cliente,tarea):
    tarea(); token=reservar(cliente)[0]['token']
    assert resultado(cliente,token).status_code==409
    assert autorizar(cliente,token).status_code==200
    assert autorizar(cliente,token).status_code==409
    assert resultado(cliente,token,'no_emitido').status_code==200
    assert resultado(cliente,token,'no_emitido').status_code==200
    nueva=reservar(cliente)[0]['token']
    assert nueva!=token
    assert resultado(cliente,token).status_code==404
    assert autorizar(cliente,nueva).status_code==200
    assert resultado(cliente,nueva).status_code==200
    assert resultado(cliente,nueva).status_code==200
    assert resultado(cliente,nueva,'no_emitido').status_code==409

def test_incierto_reinicio_y_ventana(cliente,tarea,archivo):
    tarea(); token=reservar(cliente)[0]['token']
    with TestClient(crear_app(archivo)) as otro:
        assert reservar(otro)==[]
        assert otro.get('/api/recordatorios').json()[0]['resultado']=='incierto'
    assert autorizar(cliente,token,CONTEXTO | {'ahora':'2026-10-28T00:00:00-04:00'}).status_code==409
    assert reservar(cliente,CONTEXTO | {'ahora':'2026-10-28T10:00:00-04:00'})==[]

@pytest.mark.parametrize('datos', [
    {'ahora':'ayer','zona':'America/La_Paz'}, {'ahora':'2026-10-27T09:00:00','zona':'America/La_Paz'},
    CONTEXTO|{'zona':'No/Existe'}, CONTEXTO|{'extra':1}, CONTEXTO|{'ahora':123}])
def test_contexto_invalido(cliente,datos):
    assert cliente.post('/api/recordatorios/reservar',json=datos).status_code==422

def test_resultado_y_token_invalidos(cliente,tarea):
    tarea(); token=reservar(cliente)[0]['token']
    assert resultado(cliente,'no-existe').status_code==404
    assert resultado(cliente,token,'cualquier').status_code==422
