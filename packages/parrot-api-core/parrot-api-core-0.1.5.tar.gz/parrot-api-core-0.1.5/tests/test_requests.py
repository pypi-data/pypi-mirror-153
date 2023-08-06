import responses
import pytest

url = 'http://localhost/test'
test_json = dict(result='success')
error_json = dict(error='error')
error_body = "error"
success_body = "success"


@pytest.fixture(params=[200])
def success_codes(request):
    return request.param


@pytest.fixture(params=[400, 500])
def error_codes(request):
    return request.param


@pytest.fixture(params=[dict(method="POST", response=responses.POST), dict(method="GET", response=responses.GET),
                        dict(method="PUT", response=responses.PUT), dict(method="DELETE", response=responses.DELETE)])
def request_methods(request):
    return request.param


@pytest.fixture()
def error_codes_no_json(error_codes, request_methods):
    resp = responses.Response(method=request_methods['response'], url=url, body=error_body, status=error_codes)
    return dict(resp=resp, method=request_methods['method'])


@pytest.fixture()
def error_codes_json(error_codes, request_methods):
    resp = responses.Response(method=request_methods['response'], url=url, json=error_json, status=error_codes)
    return dict(resp=resp, method=request_methods['method'])


@pytest.fixture()
def success_codes_json(success_codes, request_methods):
    resp = responses.Response(method=request_methods['response'], url=url, json=test_json,
                              status=success_codes)
    return dict(resp=resp, method=request_methods['method'])


@pytest.fixture()
def success_codes_no_json(request_methods, success_codes):
    resp = responses.Response(method=request_methods['response'], url=url, body=success_body,
                              status=success_codes)
    return dict(resp=resp, method=request_methods['method'])


@responses.activate
def test_request_success(success_codes_json):
    from parrot_api.core.requests import safe_json_request
    responses.add(success_codes_json['resp'])
    status_code, js = safe_json_request(method=success_codes_json['method'], url=url)
    assert 200 <= status_code < 300
    assert js == test_json


@responses.activate
def test_request_no_json(success_codes_no_json):
    from parrot_api.core.requests import safe_json_request
    responses.add(success_codes_no_json['resp'])
    status_code, js = safe_json_request(method=success_codes_no_json['method'], url=url)
    assert 200 <= status_code < 300
    assert js == dict(content=success_body)


@responses.activate
def test_request_failure_codes_json(error_codes_json):
    from parrot_api.core.requests import safe_json_request
    responses.add(error_codes_json['resp'])
    status_code, js = safe_json_request(method=error_codes_json['method'], url=url)
    assert 400 <= status_code < 600
    assert js == error_json


@responses.activate
def test_request_failure_codes_no_json(error_codes_no_json):
    from parrot_api.core.requests import safe_json_request
    responses.add(error_codes_no_json['resp'])
    status_code, js = safe_json_request(method=error_codes_no_json['method'], url=url)
    assert 400 <= status_code < 600
    assert js == dict(content=error_body)


@responses.activate
def test_request_retries_server_error_automatically(request_methods):
    from parrot_api.core.requests import safe_json_request
    responses.add(responses.Response(method=request_methods['response'], url=url, body=error_body, status=500))
    responses.add(responses.Response(method=request_methods['response'], url=url, json=test_json, status=200))
    status_code, js = safe_json_request(method=request_methods['response'], url=url)
    assert status_code == 200


@responses.activate
def test_request_timeout_return_code_empty_dict(request_methods):
    from parrot_api.core.requests import safe_json_request
    status_code, js = safe_json_request(method=request_methods['response'], url=url)
    assert status_code is None
    assert js == dict()
