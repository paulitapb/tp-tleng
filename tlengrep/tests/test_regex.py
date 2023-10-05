from os.path import dirname, basename, join
import glob
import importlib
import pytest
import re

# Setup: Genera los casos de test a partir de los archivos en tests/regexes/*.py
case_names = [
    basename(filename)[:-3]
    for filename in
    glob.glob(join(dirname(__file__), "regexes/*.py"))
]
case_names.sort()
cases = []
for case_name in case_names:
    regex_module = importlib.import_module(f"tests.regexes.{case_name}")
    cases.append({
        "name": case_name,
        "regex": regex_module.__regex__,
        "should_match": regex_module.__should_match__,
        "min_afnd_size": regex_module.__min_afd_size__,
    })


# Casos de test
class TestRegex:

    @pytest.mark.parametrize("case", cases, ids=lambda case: f"{case['name']}:{case['regex']}")
    def test_match(self, case, strings):
        '''Se aceptan las cadenas correctas'''
        regex = case["regex"]
        for string in strings:
            does_match = regex.match(string)
            if type(case["should_match"]) is str:
                should_match = re.fullmatch(
                    case["should_match"], string) is not None
            else:
                should_match = case["should_match"](string)
            assert does_match == should_match, f"La regex '{case['regex']}' {'no acepta' if should_match else 'acepta'} la cadena '{string}'"

    @pytest.mark.parametrize("case", cases, ids=lambda case: f"{case['name']}:{case['regex']}")
    def test_min_afd_size(self, case):
        '''El tamaño del AFD mínimo es el esperado'''
        regex = case["regex"]
        expected_min_afnd_size = case["min_afnd_size"]
        actual_min_afnd_size = regex.to_afnd().determinize().minimize().size()
        assert actual_min_afnd_size == expected_min_afnd_size, f"El AFD mínimo de la regex '{regex}' debería tener {expected_min_afnd_size} estados pero tiene {actual_min_afnd_size}"

