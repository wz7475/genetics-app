import os
from pytest import fixture

from algorithmworkers.pangolin.main import Pangolin
from tests.config import PATH_TO_DATA


@fixture
def pangolin():
    return Pangolin()


def test_pangolin_should_correctly_create_input_file(pangolin):
    pangolin.prepare_input(PATH_TO_DATA + '/pangolin_input.csv')
    assert open(PATH_TO_DATA + '/pangolin_input.csv', 'r').read() == open(pangolin.get_alg_input_name(), 'r').read()


def test_pangolin_should_correctly_create_output(pangolin):
    pangolin.prepare_output(PATH_TO_DATA + '/pangolin_output.csv')
    assert open(PATH_TO_DATA + '/pangolin_output.csv', 'r').read() == open(pangolin.get_alg_output_name(), 'r').read()
