"""Deja los reportes de cobertura listos para que SonarQube los lea.

NO BORRAR: sin este paso el analisis corre sin errores pero reporta 0% de
cobertura, que es el sintoma mas confuso posible porque parece que el proyecto
no tuviera tests. El ci.yml tambien lo invoca.

Por que hace falta: pytest corre dentro de backend/ y vitest dentro de
frontend/, asi que ambos escriben rutas relativas a su propia carpeta. SonarQube
las resuelve desde la raiz del repositorio. No se puede arreglar desde la
configuracion porque los reportes ya vienen escritos asi.

Que corrige:

  frontend/coverage/lcov.info
      'SF:src\\lib\\api.ts'  ->  'SF:frontend/src/lib/api.ts'
      (Vitest en Windows escribe barras invertidas; el scanner corre en Linux)

  backend/coverage.xml
      <source>C:\\...\\backend</source>  ->  <source>backend</source>
      (coverage.py escribe la ruta absoluta de la maquina que lo genero, que no
      existe dentro del contenedor del scanner)

Es idempotente: correrlo dos veces no rompe nada.

    python scripts/preparar_cobertura.py
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LCOV = os.path.join(RAIZ, "frontend", "coverage", "lcov.info")
COBERTURA_XML = os.path.join(RAIZ, "backend", "coverage.xml")


def arreglar_lcov():
    if not os.path.isfile(LCOV):
        print("[frontend] falta %s — corre antes: npm run test:coverage" % LCOV)
        return False

    with io.open(LCOV, encoding="utf-8") as fh:
        lineas = fh.read().splitlines()

    salida, ajustadas = [], 0
    for linea in lineas:
        if linea.startswith("SF:"):
            archivo = linea[3:].replace(chr(92), "/")
            if not archivo.startswith("frontend/"):
                archivo = "frontend/" + archivo
            linea = "SF:" + archivo
            ajustadas += 1
        salida.append(linea)

    with io.open(LCOV, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(salida) + "\n")

    faltantes = [
        linea[3:] for linea in salida
        if linea.startswith("SF:")
        and not os.path.isfile(os.path.join(RAIZ, linea[3:]))
    ]
    print("[frontend] %d rutas ajustadas" % ajustadas)
    if faltantes:
        print("[frontend] ADVERTENCIA: %d rutas no existen en disco:" % len(faltantes))
        for f in faltantes[:5]:
            print("             %s" % f)
        return False
    return True


def arreglar_coverage_xml():
    if not os.path.isfile(COBERTURA_XML):
        print("[backend] falta %s — corre antes: pytest tests/ --cov --cov-report=xml"
              % COBERTURA_XML)
        return False

    with io.open(COBERTURA_XML, encoding="utf-8") as fh:
        contenido = fh.read()

    nuevo, n = re.subn(
        r"<source>.*?</source>",
        "<source>backend</source>",
        contenido,
        flags=re.DOTALL,
    )

    if n:
        with io.open(COBERTURA_XML, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(nuevo)
        print("[backend]  <source> reescrito a 'backend' (%d ocurrencia(s))" % n)
    else:
        print("[backend]  ADVERTENCIA: no se encontro <source> en el XML")
        return False
    return True


if __name__ == "__main__":
    ok_front = arreglar_lcov()
    ok_back = arreglar_coverage_xml()
    if ok_front and ok_back:
        print("\nListo. Ya puedes lanzar el scanner.")
        sys.exit(0)
    print("\nHay reportes faltantes o con problemas; revisa los mensajes de arriba.")
    sys.exit(1)
