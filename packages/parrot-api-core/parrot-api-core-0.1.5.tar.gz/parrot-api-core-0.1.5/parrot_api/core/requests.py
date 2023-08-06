import requests
import json
from tenacity import retry, stop_after_attempt, after_log, wait_random_exponential
from parrot_api.core import log_event


def safe_json_request(method, url, log_input=False, run_async=False, **kwargs):
    """Convenience function for calling external APIs to simplify error handling.

    :param method: HTTP methond (GET, POST, PUT, etc.)
    :param url: Request URL.
    :param kwargs: Additional parameters. See requests.request for details.
    :return: tuple of status_code and json body as a python dict
    """
    import json

    log_payload = dict(url=url, method=method)
    if log_input:
        log_payload['url_params'] = kwargs.get('url_params')
        log_payload['json'] = kwargs.get('json')
    if run_async:
        return make_async_request_wrapper(method=method, url=url, log_payload=log_payload, **kwargs)
    else:
        return make_sync_request_wrapper(method=method, url=url, log_payload=log_payload, **kwargs)


def make_sync_request_wrapper(method, url, log_payload, **kwargs):
    from requests import HTTPError, ConnectionError
    try:
        response = make_sync_request(method=method, url=url, log_payload=log_payload, **kwargs)
    except ConnectionError:
        status_code = None
        js = dict()
    except HTTPError as exc:
        resp = json.loads(exc.args[0])
        status_code = resp['status_code']
        js = resp['response']
    else:
        status_code = response.status_code
        js = format_response_body(response=response)
    return status_code, js


@retry(stop=stop_after_attempt(3), reraise=True, wait=wait_random_exponential(multiplier=.1, max=1))
def make_sync_request(method, url, log_payload, **kwargs):
    from requests.exceptions import HTTPError
    try:
        r = requests.request(method=method, url=url, **kwargs)
    except ConnectionError as e:
        log_event(level='warning', status='failure', process_type='http_request', payload=log_payload)
        raise e
    else:
        log_payload['status_code'] = r.status_code
        if r.status_code >= 400:
            results = json.dumps(
                dict(
                    status_code=r.status_code,
                    response=format_response_body(response=r)
                )
            )
            log_payload['response'] = format_response_body(response=r)
            log_event(level='warning', status='failure', process_type='request',
                      payload=log_payload)
            raise HTTPError(
                results
            )
        else:
            log_event(level='debug', status='success', process_type='request', payload=log_payload)
        return r


def format_response_body(response):
    js = dict()
    try:
        js = response.json()
    except ValueError:
        js['content'] = response.text
    return js


async def format_async_response_body(response):
    js = dict()
    try:
        js = await response.json()
    except ValueError:
        js['content'] = await response.text()
    return js


async def make_async_request_wrapper(method, url, log_payload, **kwargs):
    from aiohttp.web import HTTPError, HTTPRequestTimeout

    try:
        response = await make_async_request(method=method, url=url, log_payload=log_payload, **kwargs)
    except HTTPRequestTimeout:
        status_code = None
        js = dict()
    except HTTPError as exc:
        resp = json.loads(exc.args[0])
        status_code = resp['status_code']
        js = resp['response']
    else:
        status_code = response.status_code
        js = await format_async_response_body(response=response)
    return status_code, js


@retry(stop=stop_after_attempt(3), reraise=True, wait=wait_random_exponential(multiplier=.1, max=1))
async def make_async_request(method, url, log_payload, **kwargs):
    from aiohttp.web import HTTPError, HTTPRequestTimeout
    from asyncio import get_event_loop
    loop = get_event_loop()
    error = None
    resp = None
    try:
        resp = requests.request(method=method, url=url, **kwargs)
    except HTTPRequestTimeout as e:
        error = e
    else:
        log_payload['status_code'] = resp.status_code
        if log_payload['status_code'] >= 400:
            results = json.dumps(
                dict(
                    status_code=resp.status_code,
                    response=await format_async_response_body(response=resp)
                )
            )
            log_payload['response'] = await format_async_response_body(response=resp)
            error = HTTPError(reason=results)
    finally:
        await loop.run_in_executor(
            None, log_event, 'debug' if error is None else 'warning',
            'success' if error is None else 'failure', 'request', log_payload
        )
        if error:
            raise error
        return resp


def generate_oauth_headers(access_token: str) -> dict:
    """Convenience function to generate oauth stand authorization header

    :param access_token: Oauth access token
    :return: Request headers
    """
    return {'Authorization': 'Bearer ' + access_token}
