import os
from pytest import fixture

from algorithmworkers.spip.main import SPIP
from tests.config import PATH_TO_SPIP_DATA


@fixture
def spip():
    return SPIP()


def test_spip_should_correctly_prepare_input_file(spip, monkeypatch):
    monkeypatch.setattr(SPIP, 'get_alg_input_name', lambda _: os.path.join('tests', 'data', 'spip', 'input.csv'))
    spip.prepare_input(PATH_TO_SPIP_DATA + '/spip_input.tsv')
    with open(PATH_TO_SPIP_DATA + '/spip_input_expected.csv', 'r') as expected, open(PATH_TO_SPIP_DATA + '/input.csv', 'r') as result:
        assert expected.read() == result.read()
