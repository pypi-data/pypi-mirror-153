TOKEN_NAMESPACE = 'access_tokens'


def get_audience(service_name=None) -> str:
    from parrot_api.core import get_settings
    app_settings = get_settings()
    if service_name is None:
        service_name = app_settings.get('service_name')
    audience = app_settings['audience_format'].format(service_name)
    return audience


def check_token_cache(client_id, client_secret, audience, auth_server=None):
    from datetime import datetime
    from parrot_api.core import get_memo
    now = datetime.utcnow()
    existing_token = get_memo(namespace=TOKEN_NAMESPACE,
                              kwargs=dict(client_id=client_id, client_secret=client_secret, audience=audience,
                                          auth_server=auth_server), log_inputs=False, log_value=False)
    access_token = None
    if existing_token and existing_token['expires'] > int(now.utcnow().timestamp()):
        access_token = existing_token['token']
    return access_token


def cache_token(token_response, audience, client_id, client_secret, auth_server=None):
    from datetime import datetime
    from parrot_api.core import set_memo

    set_memo(
        namespace=TOKEN_NAMESPACE, value=dict(
            token=token_response['access_token'],
            expires=int(
                datetime.utcnow().timestamp() + token_response['expires_in'] * .8)
        ),
        kwargs=dict(audience=audience, auth_server=auth_server, client_id=client_id, client_secret=client_secret),
        log_inputs=False, log_value=False

    )

    return token_response['access_token']


def get_auth_keys():
    from parrot_api.core import safe_json_request, get_settings, get_memo, set_memo
    memo_namespace = 'auth_keys'
    auth_keys = get_memo(namespace=memo_namespace, log_inputs=False, log_value=False)
    if auth_keys is None:
        status_code, js = safe_json_request(method='GET',
                                            url=get_settings()['auth_keys_url'])
        if js:
            auth_keys = js['keys']
            set_memo(namespace=memo_namespace, value=auth_keys, log_inputs=False, log_value=False)
    return auth_keys


def get_service_access_token(client_id=None, client_secret=None, auth_server=None, refresh=False, provider=None,
                             audience=None, service_name=None):
    from parrot_api.core import get_settings
    app_settings = get_settings()
    audience = get_audience(service_name=service_name) if service_name is not None and audience is None else audience
    if client_id is None or client_secret is None:
        client_id = app_settings['client_id']
        client_secret = app_settings['client_secret']
    auth_server = auth_server if auth_server is not None else app_settings['auth_server']
    token = check_token_cache(audience=audience, client_id=client_id, client_secret=client_secret,
                              auth_server=auth_server)
    if token is None or refresh:
        token_status, token_response = get_token(
            audience=audience, client_id=client_id, auth_server=auth_server,
            provider=provider,
            client_secret=client_secret
        )
        if token_response:
            token = cache_token(
                token_response=token_response, audience=audience, client_id=client_id,
                client_secret=client_secret, auth_server=auth_server
            )
    return token


def get_token(audience, client_id, client_secret, provider=None, auth_server=None):
    from parrot_api.core import get_settings
    import importlib
    app_settings = get_settings()
    auth_server = auth_server if auth_server is not None else app_settings['auth_server']
    provider = app_settings['auth_provider'] if provider is None else provider
    provider_mod = importlib.import_module('parrot_api.core.auth.providers.{provider}'.format(provider=provider))
    token_status, token_response = provider_mod.get_token(audience=audience, client_id=client_id,
                                                          auth_server=auth_server,
                                                          client_secret=client_secret)
    return token_status, token_response


def verify_token(token):
    from jose import jwt
    from .jwt import decode_token
    from werkzeug.exceptions import Unauthorized
    from parrot_api.core import get_settings
    import six
    app_settings = get_settings()
    keys = get_auth_keys()
    if not keys:
        raise Unauthorized
    try:
        decoded_token = decode_token(
            token=token, auth_keys=keys, audiences=app_settings['audiences'],
            issuers=app_settings['issuers']
        )
    except jwt.JWTError as e:
        six.raise_from(Unauthorized, e)
    else:
        if decoded_token.get('scope') is None and decoded_token.get('scp') is not None:
            decoded_token['scope'] = decoded_token['scp']
        return decoded_token


def handle_token_request(user, body):
    from connexion import request
    token_status, token_response = get_token(
        client_id=user,
        client_secret=request.authorization.password,
        audience=get_audience(),
    )
    return token_response, token_status


def verify_auth(username, password, required_scopes=None):
    return {'sub': username, 'scope': ''}


async def verify_token_async(token):
    from jose import jwt
    from parrot_api.core.auth.jwt import decode_token
    from aiohttp.web import HTTPUnauthorized
    from parrot_api.core import get_settings
    import six
    app_settings = get_settings()
    keys = await get_auth_keys_async()
    if not keys:
        raise HTTPUnauthorized
    try:
        decoded_token = decode_token(
            token=token, auth_keys=keys, audiences=app_settings['audiences'],
            issuers=app_settings['issuers']
        )
    except jwt.JWTError as e:
        six.raise_from(HTTPUnauthorized, e)
    else:
        if decoded_token.get('scope') is None and decoded_token.get('scp') is not None:
            decoded_token['scope'] = decoded_token['scp']
        return decoded_token


async def get_auth_keys_async():
    from parrot_api.core import get_settings
    from parrot_api.core.requests import safe_json_request
    from parrot_api.core import get_memo, set_memo
    memo_namespace = 'auth_keys'
    auth_keys = get_memo(namespace=memo_namespace, log_inputs=False, log_value=False)
    if auth_keys is None:
        status_code, js = await safe_json_request(method='GET',
                                                  url=get_settings()['auth_keys_url'], run_async=True)
        if js:
            auth_keys = js['keys']
            set_memo(namespace=memo_namespace, value=auth_keys, log_inputs=False, log_value=False)
    return auth_keys
