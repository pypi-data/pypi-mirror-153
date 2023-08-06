from aioresponses import aioresponses
import pytest

url = 'http://localhost/test'
test_json = dict(result='success')
error_json = dict(error='error')
error_body = "error"
success_body = "success"

@pytest.fixture()
def mocked():
    return aioresponses()


@pytest.fixture(params=[200])
def success_codes(request):
    return request.param


@pytest.fixture(params=[400, 500])
def error_codes(request):
    return request.param


@pytest.fixture(params=['put', 'post', 'patch', 'get', 'delete'])
def request_methods(request):
    return request.param


@pytest.fixture()
def error_codes_no_json(error_codes, request_methods):
    resp = dict(method=request_methods, url=url, status=error_codes, body=error_body)
    return dict(resp=resp, method=request_methods)


@pytest.fixture()
def error_codes_json(error_codes, request_methods):
    resp = dict(method=request_methods, url=url, status=error_codes, payload=error_json)
    return dict(resp=resp, method=request_methods)


@pytest.fixture()
def success_codes_json(success_codes, request_methods):
    resp = dict(method=request_methods, url=url, status=success_codes, payload=test_json)
    return dict(resp=resp, method=request_methods)


@pytest.fixture()
def success_codes_no_json(request_methods, success_codes):
    resp = dict(method=request_methods, url=url, status=success_codes, body=success_body)
    return dict(resp=resp, method=request_methods)

async def test_request_success(mocked, success_codes_json):
    from parrot_api.core.requests import safe_json_request
    with mocked:
        mocked.add(**success_codes_json['resp'])
        status_code, js = await safe_json_request(method=success_codes_json['method'], url=url, run_async=True)
        assert 200 <= status_code < 300
        assert js == test_json

async def test_request_no_json(mocked, success_codes_no_json):
    from parrot_api.core.requests import safe_json_request
    with mocked:
        mocked.add(**success_codes_no_json['resp'])
        status_code, js = await safe_json_request(method=success_codes_no_json['method'], url=url, run_async=True)
        assert 200 <= status_code < 300
        assert js == dict(content=success_body)

async def test_request_failure_codes_json(mocked, error_codes_json):
    from parrot_api.core.requests import safe_json_request
    with mocked:

        mocked.add(**error_codes_json['resp'])
        mocked.add(**error_codes_json['resp'])
        mocked.add(**error_codes_json['resp'])

        status_code, js = await safe_json_request(method=error_codes_json['method'], url=url, run_async=True)
        assert 400 <= status_code < 600
        assert js == error_json

async def test_request_failure_codes_no_json(mocked, error_codes_no_json):
    from parrot_api.core.requests import safe_json_request
    with mocked:

        mocked.add(**error_codes_no_json['resp'])
        mocked.add(**error_codes_no_json['resp'])
        mocked.add(**error_codes_no_json['resp'])
        status_code, js = await safe_json_request(method=error_codes_no_json['method'], url=url, run_async=True)
        assert 400 <= status_code < 600
        assert js == dict(content=error_body)


async def test_request_retries_server_error_automatically(mocked, request_methods):
    from parrot_api.core.requests import safe_json_request
    with mocked:
        mocked.add(method=request_methods, url=url, body=error_body, status=500)
        mocked.add(method=request_methods, url=url, payload=test_json, status=200)
        status_code, js = await safe_json_request(method=request_methods, url=url, run_async=True)
        assert status_code == 200


async def test_request_timeout_return_code_empty_dict(mocked, request_methods):
    from parrot_api.core.requests import safe_json_request
    with mocked:
        status_code, js = await safe_json_request(method=request_methods, url=url, run_async=True)
        assert status_code is None
        assert js == dict()
