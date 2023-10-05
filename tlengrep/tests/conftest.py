#!/usr/bin/env python3
from os.path import dirname, basename, join
import glob

# Lista de archivos con cadenas de entrada
input_string_files = [basename(filename) for filename in glob.glob(
    join(dirname(__file__), "strings/*.txt"))]

# Extraemos las cadenas de los archivos
input_strings = []
for file in input_string_files:
    with open(join(dirname(__file__), f"strings/{file}")) as f:
        input_strings.append(f.read().splitlines())


def pytest_generate_tests(metafunc):
    """Genera los tests parametrizados con las cadenas de entrada"""
    if "strings" in metafunc.fixturenames:
        metafunc.parametrize("strings", input_strings, ids=input_string_files)
