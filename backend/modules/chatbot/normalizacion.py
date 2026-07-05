"""Normalización de texto para el match exacto de la whitelist.

Módulo sin dependencias externas para poder importarlo desde los tests
sin arrastrar langchain ni la configuración del backend (core.config).
"""

import re
import unicodedata

_PUNTUACION = re.compile(r"[¿?¡!.,;:\"'()]")
_ESPACIOS = re.compile(r"\s+")


def normalizar_texto(texto: str) -> str:
    """Minúsculas, sin tildes, sin puntuación y con espacios colapsados.

    Así "¡Chao!" y "chao" quedan iguales y el match exacto contra la
    whitelist es determinístico, sin depender de la distancia de embeddings
    (que con palabras muy cortas puede confundir "chao" con "hola").
    """
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = _PUNTUACION.sub("", texto)
    texto = _ESPACIOS.sub(" ", texto)
    return texto.strip()
