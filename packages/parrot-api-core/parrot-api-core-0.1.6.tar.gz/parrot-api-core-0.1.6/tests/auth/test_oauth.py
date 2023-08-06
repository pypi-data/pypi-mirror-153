import responses


def test_audience(app_settings):
    from parrot_api.core.auth.oauth import get_audience
    assert get_audience('hello') == 'http://hello/api'


def test_default_audience(app_settings):
    from parrot_api.core.auth.oauth import get_audience
    assert get_audience() == 'http://test/api'


@responses.activate
def test_auth_cache(app_settings):
    from parrot_api.core.auth.oauth import get_service_access_token
    responses.add(
        responses.Response(method=responses.POST, url=app_settings['auth_server'],
                           json=dict(access_token='1', expires_in=86400),
                           status=200))
    responses.add(
        responses.Response(method=responses.POST, url=app_settings['auth_server'],
                           json=dict(access_token='2', expires_in=86400),
                           status=200))
    token_a = get_service_access_token(service_name='test')
    token_b = get_service_access_token(service_name='test')
    assert token_a == token_b


@responses.activate
def test_auth_cache_expiration(app_settings):
    from parrot_api.core.auth.oauth import get_service_access_token
    responses.add(
        responses.Response(method=responses.POST, url=app_settings['auth_server'],
                           json=dict(access_token='1', expires_in=0), status=200)
    )
    responses.add(
        responses.Response(method=responses.POST, url=app_settings['auth_server'],
                           json=dict(access_token='2', expires_in=300), status=200)
    )
    token_a = get_service_access_token(service_name='test_2')
    token_b = get_service_access_token(service_name='test_2')
    assert token_a != token_b


@responses.activate
def test_valid_token(client, valid_access_headers, public_keys, app_settings):
    responses.add(
        responses.Response(method=responses.GET, url=app_settings['auth_keys_url'],
                           json=public_keys, status=200)
    )
    resp = client.get('/v1/hello', headers=valid_access_headers)
    assert resp.status_code == 200


@responses.activate
def test_invalid_token(client, invalid_access_headers, public_keys, app_settings):
    responses.add(
        responses.Response(method=responses.GET, url=app_settings['auth_keys_url'],
                           json=public_keys, status=200)
    )
    resp = client.get('/v1/hello', headers=invalid_access_headers)
    assert resp.status_code == 401


@responses.activate
def test_unauthorized_token(client, unauthorized_access_headers, public_keys, app_settings):
    responses.add(
        responses.Response(method=responses.GET, url=app_settings['auth_keys_url'],
                           json=public_keys, status=200)
    )
    resp = client.get('/v1/hello', headers=unauthorized_access_headers)
    assert resp.status_code == 403


@responses.activate
def test_unauthorized_token(client, unauthorized_access_headers, public_keys, app_settings):
    responses.add(
        responses.Response(method=responses.GET, url=app_settings['auth_keys_url'],
                           json=public_keys, status=200)
    )
    resp = client.get('/v1/hello', headers=unauthorized_access_headers)
    assert resp.status_code == 403


@responses.activate
def test_invalid_user_token(client, user_access_headers, public_keys, app_settings):
    responses.add(
        responses.Response(method=responses.GET, url=app_settings['auth_keys_url'],
                           json=public_keys, status=200)
    )
    responses.add(
        responses.Response(method=responses.POST, url=app_settings['user_scopes_api'],
                           json=dict(active=True, response=dict()), status=403)
    )
    resp = client.get('/v1/hello', headers=user_access_headers)
    assert resp.status_code == 403


@responses.activate
def test_unauthorized_user_token(client, user_access_headers, public_keys, app_settings):
    responses.add(
        responses.Response(method=responses.GET, url=app_settings['auth_keys_url'],
                           json=public_keys, status=200)
    )
    responses.add(
        responses.Response(method=responses.POST, url=app_settings['user_scopes_api'],
                           json=dict(active=True, response=dict(available_scopes=[])), status=200)
    )
    resp = client.get('/v1/hello', headers=user_access_headers)
    assert resp.status_code == 403


@responses.activate
def test_echo_user_token(client, user_access_headers, public_keys, app_settings):
    responses.add(
        responses.Response(method=responses.GET, url=app_settings['auth_keys_url'],
                           json=public_keys, status=200)
    )
    responses.add(
        responses.Response(method=responses.POST, url=app_settings['user_scopes_api'],
                           json=dict(active=True, response=dict(available_scopes=['get:hello'])), status=200)
    )
    resp = client.get('/v1/echo_token', headers=user_access_headers)
    assert resp.status_code == 200
    assert resp.json['response'] == user_access_headers['Authorization'].split(' ')[-1]
