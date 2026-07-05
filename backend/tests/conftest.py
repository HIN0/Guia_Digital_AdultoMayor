"""Configuración de pytest: agrega backend/ al sys.path para poder importar
los paquetes del proyecto (modules, core) igual que lo hace main.py.

Ejecutar desde la carpeta backend/:  python -m pytest tests/ -v
Requiere:  pip install pytest
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
