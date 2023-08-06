import json
import pytest
import os


DATA_DIR = f'{os.getcwd()}/tests'


@pytest.fixture
def config():
    config = json.load(open(f'{DATA_DIR}/config.json'))
    return config
