"""
These tests work on any integrations using BasicRest classes
"""

import json
import pytest
from jsonschema import validate
from .output_verify import OUTPUT_MAP
import functools
from unittest.mock import patch
from requests import Session
import pickle
from deepdiff import DeepDiff
import os
import sys
import re
import copy
import importlib
from io import BytesIO
from .constants import FALSY_VALUES

# For shell execution
sys.path.append(os.getcwd())

# Globals
TEST_DIR = f'{os.getcwd()}/tests'
DATA_DIR = f'{os.getcwd()}/data'

def get_task_names():
    tasks = [x.replace('.py', '') for x in os.listdir(f'{os.getcwd()}/imports') if x.endswith('.py')]
    # asset is its own test
    if 'asset' in tasks:
        tasks.remove('asset')
    return tasks


def gather_test_dirs(task):
    tests = []
    if os.path.exists(os.path.join(TEST_DIR, task)):
        tests = [d for d in os.listdir(os.path.join(TEST_DIR, task)) if re.findall(r'test_.+', d)]
    return tests


def gather_tests():
    tests = []
    for task in get_task_names():
        for test in gather_test_dirs(task):
            tests.append((task, test))
    return tests


def bytes_to_string(data):
    if isinstance(data, (list, tuple)):
        return [bytes_to_string(element) for element in data]
    elif isinstance(data, dict):
        return {key: bytes_to_string(value) for key, value in data.items()}
    if isinstance(data, bytes):
        return str(data.hex())
    if isinstance(data, BytesIO):
        return data.read().hex()
    else:
        return data


def create_comparable_request(data):
    data['kwargs'].pop('headers', None)
    data['kwargs'].pop('auth', None)
    data = bytes_to_string(data)
    return data


def get_test_config(task, test):
    """
    Get the config for the test
    """
    file_path = f'{TEST_DIR}/{task}/{test}/config.json'
    config = {}
    if os.path.exists(file_path):
        config = json.load(open(file_path, 'r'))
    return config


def get_mock_data(task, test):
    """
    Get the mock data for the test
    """
    file_path = f'{TEST_DIR}/{task}/{test}/mocks.json'
    mocks = []
    if os.path.exists(file_path):
        mocks = json.load(open(file_path, 'r'))
    return mocks


def build_mock(mock_definitions, auth_endpoints):

    def mock_handler(self, *args, **kwargs):
        comparable = {
            "args": list(args),
            "kwargs": kwargs
        }
        comparable = create_comparable_request(comparable)
        url = kwargs.get('url')
        if not url:
            url = args[1]
        if auth_endpoints and any([endpoint in url for endpoint in auth_endpoints]):
            comparable['kwargs'] = {}
        for request in mock_definitions:
            if DeepDiff(comparable, request['request']) == {}:
                return pickle.loads(bytes.fromhex(request["response"]))
        else:
            raise (Exception(f"No mock found for request args: {args}, kwargs: {kwargs}"))

    return mock_handler


def mock_session(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if func.__name__.startswith("test") and args[0].test_config.get("mock_requests")\
                and not args[0].global_config.get("mock_requests"):
            print("Test override: forcing mock_requests")
        if args[0].config.get('mock_requests', False):
            with patch.object(Session, 'request', build_mock(args[0].mocks, args[0].config['auth_endpoints'])):
                return func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper


def sw_main(task, _inputs, _asset):
    mod = importlib.import_module(f'imports.{task}')
    if not _asset:
        _asset = json.loads(open(f'{DATA_DIR}/asset.json').read())

    class Context:
        asset = _asset
        inputs = _inputs

    # We did a big dumb and defaulted kwargs to {} in BasicRestEndpoint, which is a mutable object.
    #  Because kwargs is mutable, every test is modifying the same kwargs if it only does updates.
    #  This resets kwargs back to an empty dict after every test so we don't carry values over to subsequent tests
    if getattr(mod.SwMain, "kwargs", False):
        mod.SwMain.kwargs.clear()
    ctx = mod.SwMain(Context)
    return ctx


@pytest.mark.parametrize("task, test", gather_tests())
class TestStandardRest:

    @pytest.fixture(autouse=True)
    def _set_ctx(self, task, test, config):
        # Test setup before yield
        self.task = task
        self.test = test
        self.mocks = get_mock_data(task, test)
        self.test_config = get_test_config(task, test)
        self.global_config = config
        self.config = copy.deepcopy(self.global_config)
        self.config.update(self.test_config)
        self.ctx = self.cls(task, test)

    @mock_session
    def cls(self, task, test):
        """Instantiate SwMain for general tests"""
        inputs = json.load(open(f'{TEST_DIR}/{task}/{test}/inputs.json')) if task != 'asset' else {}
        return sw_main(task, inputs, None)

    def test_kwargs(self, *args, **kwargs):
        """
        This will test the payload schema json, params, data, files, etc. As utils passes it.
        """
        if self.config.get('validate_kwargs') == False:
            pytest.skip("validate_kwargs config is False. Skipping test.")
        schema = json.loads(open(f'{TEST_DIR}/{self.task}/schemas/kwargs.json').read())
        validate(
            instance=self.ctx.get_kwargs(),
            schema=schema
        )

    def test_session_headers(self, test, *args, **kwargs):
        """
        Verify session headers against schema
        """
        # check if local header schema, this overrides global.
        if self.config.get('validate_headers') == False:
            pytest.skip("validate_headers config is False. Skipping test.")
        try:
            schema = json.loads(open(f'{TEST_DIR}/{self.task}/schemas/headers.json').read())
        except:
            schema = False
        if not schema:
            # check if global schema
            schema = json.loads(open(f'{TEST_DIR}/headers.json').read())
            if not schema:
                raise ValueError(
                    'Must define the header schema globally or specifically in the task.'
                )
        validate(
            instance=dict(self.ctx.session.headers),
            schema=schema
        )

    @mock_session
    def test_parse_response(self, *args, **kwargs):
        """
        Execute task and verify data to output manifest types.
        """
        resp = self.ctx.execute()
        assert self.validate_output_manifest(resp)

    def validate_output_manifest(self, resp, *args, **kwargs):
        """
        Helper function:
        Loads the task manifest and compares task results to output type schema.
        """
        missing = []  # store missing outputs
        schema = json.loads(open(f'imports/{self.task}.json').read())['availableOutputVariables']
        if isinstance(resp, dict):
            resp = [resp]
        for record in resp:
            for k, v in record.items():
                # If this is a sub key of a flattened key, ignore.
                for k2 in schema:
                    if k2.startswith(k) and k2.lstrip(k).startswith('_'):
                        break
                else:
                    _type = schema.get(k, {}).get('type')
                    if _type:
                        if v not in FALSY_VALUES and not OUTPUT_MAP[_type](v):
                            assert False, f'Output Key: {k}, Type: {_type}\nValue: {v}'
                    else:
                        missing.append(k)
        if missing and self.config.get("allow_missing_outputs") is not True:
            assert False, f'Manifest is missing outputs: {missing}'
        return True
