def get_token(client_id, client_secret, audience, auth_server):
    from parrot_api.core import safe_json_request
    body = dict(
        client_id=client_id,
        client_secret=client_secret,
        audience=audience,
        grant_type="client_credentials"
    )

    status_code, js = safe_json_request(
        url=auth_server, method='POST',
        json=body
    )
    return status_code, js
