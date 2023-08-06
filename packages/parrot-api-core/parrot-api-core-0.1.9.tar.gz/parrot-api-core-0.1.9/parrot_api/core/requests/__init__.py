def safe_json_request(method, url, log_input=False, run_async=False, **kwargs):
    """Convenience function for calling external APIs to simplify error handling.

    :param method: HTTP methond (GET, POST, PUT, etc.)
    :param url: Request URL.
    :param kwargs: Additional parameters. See requests.request for details.
    :return: tuple of status_code and json body as a python dict
    """
    import json
    from .async_ import make_async_request_wrapper
    from .sync import make_sync_request_wrapper

    log_payload = dict(url=url, method=method)
    if log_input:
        log_payload['url_params'] = kwargs.get('url_params')
        log_payload['json'] = kwargs.get('json')
    if run_async:
        return make_async_request_wrapper(method=method, url=url, log_payload=log_payload, **kwargs)
    else:
        return make_sync_request_wrapper(method=method, url=url, log_payload=log_payload, **kwargs)


def generate_oauth_headers(access_token: str) -> dict:
    """Convenience function to generate oauth stand authorization header

    :param access_token: Oauth access token
    :return: Request headers
    """
    return {'Authorization': 'Bearer ' + access_token}
