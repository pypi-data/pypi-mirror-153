import requests
import json
from tenacity import retry, stop_after_attempt, after_log, wait_random_exponential
from parrot_api.core import log_event


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
