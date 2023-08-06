def create_server(spec_dir, port=8080, debug=False, sync=True, request_context_name=None):
    import connexion
    import os
    import yaml
    from parrot_api.core.common import get_subpackage_paths

    if sync:
        app = connexion.FlaskApp(
            __name__, port=port,
            specification_dir=spec_dir, debug=debug
        )

        @app.route('/')
        def health_check():
            return home()
    else:
        app = connexion.AioHttpApp(__name__, port=8080, specification_dir=spec_dir, debug=debug)

        async def health_check(request):
            from aiohttp.web import json_response
            return json_response(home())

        app.app.router.add_get('/', health_check)

    for spec in os.listdir(spec_dir):
        app.add_api(specification=spec, validate_responses=debug, pass_context_arg_name=request_context_name)

    for path in get_subpackage_paths():
        schema_directory = os.path.join(path, 'schemas/')
        if os.path.isdir(schema_directory):
            for spec_file in [i for i in os.listdir(schema_directory) if i.endswith('yaml') or i.endswith("yml")]:
                with open(os.path.join(schema_directory, spec_file), 'rt') as f:
                    spec = yaml.safe_load(f)
                app.add_api(specification=spec, validate_responses=debug)
    return app


def home():
    return dict(status='ok')


def say_hello():
    return dict(response='hello')


async def async_hello(request):
    return dict(response='hello {token}'.format(token=request.headers['Authorization'].split(' ')[-1]))
