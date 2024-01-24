import os
from pytest import fixture

from algorithmworkers.mock_algorithm.main import Mock_Algorithm
from tests.config import PATH_TO_MOCK_ALGORITHM_DATA


@fixture
def mock_algorithm():
    return Mock_Algorithm()


def test_e2e_mock_algorithm(mock_algorithm):
    mock_algorithm.process_task(
        os.path.join(PATH_TO_MOCK_ALGORITHM_DATA, 'mock_algorithm_input.tsv'),
        os.path.join(PATH_TO_MOCK_ALGORITHM_DATA, 'mock_algorithm_output.csv'))

    with (open(os.path.join(PATH_TO_MOCK_ALGORITHM_DATA, 'mock_algorithm_input.tsv')) as expected_input,
          open(mock_algorithm.input_file_path, 'r') as algorithm_input):
        assert expected_input.read() == algorithm_input.read()

    with (open(os.path.join(PATH_TO_MOCK_ALGORITHM_DATA, 'mock_algorithm_output_expected.csv'), 'r') as expected_output,
          open(os.path.join(PATH_TO_MOCK_ALGORITHM_DATA, 'mock_algorithm_output.csv')) as algorithm_output):
        assert expected_output.read() == algorithm_output.read()
