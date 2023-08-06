import json
from tenacity import retry, stop_after_attempt, after_log, wait_random_exponential
from parrot_api.core import log_event

aiohttp_session = None


def get_session(url: str):
    import aiohttp
    import orjson
    global aiohttp_session
    if aiohttp_session is None:
        aiohttp_session = aiohttp.ClientSession(json_serialize=orjson.dumps)
    return aiohttp_session


async def format_async_response_body(response):
    js = dict()
    try:
        js = await response.json()
    except ValueError:
        js['content'] = await response.text()
    return js


async def make_async_request_wrapper(method, url, log_payload, **kwargs):
    from aiohttp.client_exceptions import ClientConnectionError, ClientResponseError

    try:
        response = await make_async_request(method=method, url=url, log_payload=log_payload, **kwargs)
    except ClientConnectionError:
        status_code = None
        js = dict()
    except ClientResponseError as e:
        status_code = e.status
        js = json.loads(e.message)
    else:
        status_code = response.status
        js = await format_async_response_body(response=response)
    return status_code, js


@retry(stop=stop_after_attempt(3), reraise=True, wait=wait_random_exponential(multiplier=.1, max=1))
async def make_async_request(method, url, log_payload, **kwargs):
    from aiohttp.client_exceptions import ClientConnectionError, ClientResponseError
    from aiohttp.web import HTTPClientError, HTTPError
    from asyncio import get_event_loop
    loop = get_event_loop()
    error = None
    resp = None
    try:
        session = get_session(url=url)
        resp = await session.request(method=method, url=url, raise_for_status=False, **kwargs)
    except (ClientConnectionError, HTTPClientError) as e:
        error = e
        log_payload['response'] = json.dumps(
            dict(
                status_code=None,
                response=dict()
            )
        )
    except ClientResponseError as e:
        error = e
        log_payload['response'] = json.dumps(
            dict(
                status_code=e.status,
                response=await format_async_response_body(e.history[0])
            )
        )
    else:
        log_payload['status_code'] = resp.status
        if log_payload['status_code'] >= 400:
            response = await format_async_response_body(response=resp)
            results = json.dumps(
                dict(
                    status_code=log_payload['status_code'],
                    response=response
                )
            )
            log_payload['response'] = response
            error = ClientResponseError(status=resp.status, message=json.dumps(response), history=(), request_info=resp.request_info)
    finally:
        await loop.run_in_executor(
            None, log_event, 'debug' if error is None else 'warning',
            'success' if error is None else 'failure', 'request', log_payload
        )

        if error:
            raise error
        return resp
