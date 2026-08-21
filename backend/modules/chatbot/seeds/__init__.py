"""
Agrupa todos los módulos de seed en un solo diccionario SEED_DATA.

PARA AGREGAR UNA PATOLOGÍA NUEVA:
  1. Crea seeds/nombre_patologia.py con un diccionario DATA = {"Nombre": [...]}
     (copia la estructura de urgencias.py como plantilla).
  2. Impórtalo abajo y agrégalo a _MODULOS.
  3. Reinicia el backend (el seed es idempotente, solo inserta lo nuevo).
No hay que tocar seed.py nunca.
"""

from . import (
    caidas,
    cefalea,
    gastroenteritis,
    general,
    glosario,
    hipertension,
    huap,
    itu,
    lumbago,
    neumonia,
)

_MODULOS = [general, gastroenteritis, neumonia, itu, cefalea, lumbago, huap, hipertension, caidas, glosario]

SEED_DATA = {}
for _modulo in _MODULOS:
    for _patologia, _preguntas in _modulo.DATA.items():
        # Si dos módulos definen la misma patología, se combinan sus preguntas
        SEED_DATA.setdefault(_patologia, []).extend(_preguntas)
