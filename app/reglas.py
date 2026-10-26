"""Reglas de texto y tiempo, independientes del transporte."""
import re
import unicodedata
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

COLORES = ('azul', 'verde', 'rojo', 'naranja', 'morado', 'turquesa')

def normalizar_texto(valor: str, maximo: int, opcional=False) -> str:
    if not isinstance(valor, str):
        raise ValueError('Debe ser texto')
    texto = unicodedata.normalize('NFC', valor)
    if not opcional:
        texto = texto.strip()
    elif not texto.strip():
        texto = ''
    if '\x00' in texto or len(texto) > maximo or (not opcional and not texto):
        raise ValueError(f'Ingresa texto de {0 if opcional else 1} a {maximo} caracteres, sin carácter NUL')
    return texto

def fecha_valida(valor: str) -> str:
    if not isinstance(valor, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', valor):
        raise ValueError('Ingresa una fecha válida en formato AAAA-MM-DD')
    date.fromisoformat(valor)
    return valor

def ventana_recordatorio(fecha: str, ahora: datetime, zona: str) -> bool:
    local = ahora.astimezone(ZoneInfo(zona))
    entrega = date.fromisoformat(fecha)
    return local.date() == entrega - timedelta(days=1) and local.hour >= 9
