"""Validación del dominio y calendario local, sin reloj del servidor."""
from datetime import datetime
from zoneinfo import ZoneInfo
import pytest
from app.reglas import normalizar_texto, ventana_recordatorio

@pytest.mark.parametrize('valor', ['', '   ', 'a' * 101, 'x\x00y'])
def test_nombre_invalido(valor):
    with pytest.raises(ValueError):
        normalizar_texto(valor, 100)

@pytest.mark.parametrize('valor,esperado', [(' e\u0301 ', 'é'), ('😀' * 100, '😀' * 100), ('Álgebra', 'Álgebra')])
def test_normalizacion(valor, esperado):
    assert normalizar_texto(valor, 100) == esperado

@pytest.mark.parametrize('instante,esperado', [
    ('2026-10-27T08:59:59.999-04:00', False),
    ('2026-10-27T09:00:00-04:00', True),
    ('2026-10-27T23:59:59.999-04:00', True),
    ('2026-10-28T00:00:00-04:00', False),
    ('2026-10-26T10:00:00-04:00', False)])
def test_fronteras(instante, esperado):
    assert ventana_recordatorio('2026-10-28', datetime.fromisoformat(instante), 'America/La_Paz') is esperado

@pytest.mark.parametrize('fecha,instante,zona', [
    ('2027-01-01', '2026-12-31T09:00:00-04:00', 'America/La_Paz'),
    ('2028-03-01', '2028-02-29T09:00:00-04:00', 'America/La_Paz'),
    ('2026-03-09', '2026-03-08T09:00:00-04:00', 'America/New_York')])
def test_calendario(fecha, instante, zona):
    assert ventana_recordatorio(fecha, datetime.fromisoformat(instante), zona)
