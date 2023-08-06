def sign_token(payload: dict, signing_key: dict):
    from jose import jwt, constants

    headers = dict(
        typ='JWT',
        alg='RS256',
        kid=signing_key['kid']
    )
    signed_string = jwt.encode(claims=payload, headers=headers, algorithm=constants.ALGORITHMS.RS256, key=signing_key)
    return signed_string


def check_active_token(decoded_token, leeway):
    from datetime import datetime, timedelta
    from jose.exceptions import ExpiredSignatureError, JWTError
    now = datetime.utcnow()
    if int((now + timedelta(seconds=leeway)).timestamp()) < decoded_token['iat']:
        raise JWTError("Token Issued In the Future")
    if int((now - timedelta(seconds=leeway)).timestamp()) > decoded_token['exp']:
        raise ExpiredSignatureError("Token Expired")


def format_access_token(user, machine_token: bool, issuer, audiences: list, expiration_seconds: int,
                        scopes: list = None, **claims):
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    if machine_token:
        subject = '{0}@clients'.format(user)
    else:
        subject = user
    assert isinstance(audiences, list)
    body = dict(
        iss=issuer,
        sub=subject,
        azp=user,
        iat=int(now.timestamp()),
        aud=audiences if len(audiences) > 1 else audiences[0],
        exp=int((now + timedelta(seconds=expiration_seconds)).timestamp()),
        scope=' '.join(scopes if scopes is not None else []),
        gty='client-credentials',
        **claims
    )
    return {k: v for k, v in body.items() if v}


def get_rsa_key(token, auth_keys):
    from jose import jwt
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in auth_keys:
        if key.get("kid") == unverified_header.get("kid") and key.get('kid') is not None:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
            break
    return rsa_key


def decode_token(token, auth_keys, audiences, issuers, leeway=10 * 60):
    from jose import jwt
    import itertools

    payload = None
    rsa_key = get_rsa_key(token=token, auth_keys=auth_keys)

    if rsa_key:
        error = None
        for audience, issuer in itertools.product(audiences, issuers):
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    options={
                        'verify_signature': True,
                        'verify_aud': True,
                        'verify_iat': True,
                        'verify_exp': True,
                        'verify_nbf': True,
                        'verify_iss': True,
                        'verify_sub': True,
                        'verify_jti': True,
                        'verify_at_hash': True,
                        'require_aud': False,
                        'require_iat': True,
                        'require_exp': True,
                        'require_nbf': False,
                        'require_iss': True,
                        'require_sub': False,
                        'require_jti': False,
                        'require_at_hash': False,
                        'leeway': 0,
                    },
                    algorithms=["RS256"],
                    audience=audience,
                    issuer=issuer)
            except jwt.JWTError as exc:
                error = exc
            else:
                break
        if error is not None and payload is None:
            raise error
        else:
            check_active_token(decoded_token=payload, leeway=leeway)
    return payload
