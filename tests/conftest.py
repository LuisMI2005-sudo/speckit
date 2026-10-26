"""Recursos aislados: ninguna prueba modifica la agenda real."""
import socket
import threading
import time
import pytest
import uvicorn
from fastapi.testclient import TestClient
from app.main import crear_app

@pytest.fixture
def archivo(tmp_path):
    return tmp_path / "agenda.sqlite3"

@pytest.fixture
def aplicacion(archivo):
    return crear_app(archivo)

@pytest.fixture
def cliente(aplicacion):
    with TestClient(aplicacion) as client:
        yield client

@pytest.fixture
def materia(cliente):
    respuesta = cliente.post('/api/materias', json={'nombre': 'Cálculo I', 'color': 'azul'})
    assert respuesta.status_code == 201
    return respuesta.json()

@pytest.fixture
def tarea(cliente, materia):
    def crear(fecha='2026-10-28', estado='pendiente', titulo='Práctica'):
        respuesta = cliente.post('/api/tareas', json={
            'materia_id': materia['id'], 'titulo': titulo, 'fecha_entrega': fecha,
            'descripcion': 'Contenido privado que no va al aviso'})
        assert respuesta.status_code == 201
        dato = respuesta.json()
        if estado == 'completada':
            cliente.patch(f"/api/tareas/{dato['id']}/completar")
        return dato
    return crear

@pytest.fixture
def servidor(aplicacion, cliente):
    # El socket se reserva antes de arrancar para evitar carreras de puerto.
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    puerto = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(aplicacion, log_level='error'))
    thread = threading.Thread(target=server.run, kwargs={'sockets': [sock]}, daemon=True)
    thread.start()
    limite = time.monotonic() + 10
    while not server.started:
        if not thread.is_alive() or time.monotonic() > limite:
            raise RuntimeError('No inició el servidor de pruebas')
        time.sleep(.02)
    yield f'http://127.0.0.1:{puerto}'
    server.should_exit = True
    thread.join(10)
    sock.close()
    assert not thread.is_alive()
