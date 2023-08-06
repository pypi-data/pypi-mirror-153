import pytest
from parrot_api.core.common import generate_random_id


@pytest.fixture()
def claims(audience, issuer):
    from parrot_api.core.auth.jwt import format_access_token
    from parrot_api.core.common import generate_random_id

    return format_access_token(
        user=generate_random_id(), machine_token=True, audiences=[audience], issuer=issuer, expiration_seconds=60 * 60,
        scopes=[generate_random_id() for i in range(3)]
    )


@pytest.fixture()
def future_token(claims, audience, issuer, signing_key):
    from datetime import datetime, timedelta
    from parrot_api.core.auth.jwt import sign_token
    from copy import deepcopy
    claims = deepcopy(claims)
    claims['iat'] = int((datetime.fromtimestamp(claims['iat']) + timedelta(days=1)).timestamp())
    claims['exp'] = int((datetime.fromtimestamp(claims['exp']) + timedelta(days=1)).timestamp())
    token = sign_token(payload=claims, signing_key=signing_key)
    return token


@pytest.fixture()
def expired_token(claims, audience, issuer, signing_key):
    from datetime import datetime, timedelta
    from parrot_api.core.auth.jwt import sign_token
    from copy import deepcopy
    claims = deepcopy(claims)
    claims['iat'] = int((datetime.fromtimestamp(claims['iat']) - timedelta(days=1)).timestamp())
    claims['exp'] = int((datetime.fromtimestamp(claims['exp']) - timedelta(days=1)).timestamp())
    token = sign_token(payload=claims, signing_key=signing_key)
    return token


@pytest.fixture()
def signed_token(claims, audience, issuer, signing_key):
    from parrot_api.core.auth.jwt import sign_token
    token = sign_token(payload=claims, signing_key=signing_key)
    return token


def test_decode_token(claims, public_keys, signed_token, audiences, issuers):
    from parrot_api.core.auth.jwt import decode_token
    decoded_token = decode_token(token=signed_token, audiences=audiences, issuers=issuers,
                                             auth_keys=public_keys['keys'])
    assert claims == decoded_token


def test_invalid_issuer(signed_token, public_keys, audiences):
    from parrot_api.core.auth.jwt import decode_token
    from jose.exceptions import JWTError
    with pytest.raises(JWTError):
        decode_token(
            token=signed_token, audiences=audiences, issuers=[generate_random_id()],
            auth_keys=public_keys['keys']
        )


def test_invalid_audience(signed_token, public_keys, issuers):
    from parrot_api.core.auth.jwt import decode_token
    from jose.exceptions import JWTError
    with pytest.raises(JWTError):
        decode_token(token=signed_token, audiences=[generate_random_id()], issuers=issuers,
                     auth_keys=public_keys['keys'])


def test_expired_token(expired_token, public_keys, audiences, issuers):
    from parrot_api.core.auth.jwt import decode_token
    from jose.exceptions import ExpiredSignatureError
    with pytest.raises(ExpiredSignatureError):
        decode_token(
            token=expired_token, audiences=audiences, issuers=issuers,
            auth_keys=public_keys['keys']
        )


def test_future_token(future_token, public_keys, audiences, issuers):
    from parrot_api.core.auth.jwt import decode_token
    from jose.exceptions import JWTError
    with pytest.raises(JWTError):
        decode_token(
            token=future_token, audiences=audiences, issuers=issuers,
            auth_keys=public_keys['keys']
        )
