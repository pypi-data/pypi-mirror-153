def echo_access_token():
    from parrot_api.core.auth.oauth import get_service_access_token
    from parrot_api.core.settings import get_settings
    from connexion import context
    print(context.get('user'))
    return dict(active=True, response=get_service_access_token(service_name=get_settings()['service_name']))
