import os
from pytest import fixture

from algorithmworkers.pangolin.main import Pangolin
from tests.config import PATH_TO_PANGOLIN_DATA


@fixture
def pangolin():
    return Pangolin()


def test_pangolin_should_correctly_prepare_input_file(pangolin, monkeypatch):
    monkeypatch.setattr(Pangolin, 'get_alg_input_name', lambda _: os.path.join('tests', 'data', 'pangolin', 'input.csv'))
    pangolin.prepare_input(PATH_TO_PANGOLIN_DATA + '/pangolin_input.tsv')
    with (open(PATH_TO_PANGOLIN_DATA + '/pangolin_input_expected.csv', 'r') as expected,
          open(PATH_TO_PANGOLIN_DATA + '/input.csv', 'r') as result):
        assert expected.read() == result.read()
