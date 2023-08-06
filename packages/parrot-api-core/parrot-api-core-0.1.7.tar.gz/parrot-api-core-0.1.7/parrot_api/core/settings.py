__settings__ = None


def get_settings(settings_type='app', env_folder=None, refresh=False):
    import os
    import json
    from parrot_api.core.common import generate_random_id
    from .logging import log_event
    global __settings__

    if __settings__ is None or refresh:
        folder = env_folder if env_folder is not None else os.getenv('ENV_FOLDER')
        settings = dict()

        for root, dirs, files in os.walk(folder, topdown=True):
            dirs.sort()
            for file in files:
                file_type = file.replace('.json', '')
                if file_type not in settings.keys():
                    settings[file_type] = dict()
                local_path = os.path.join(folder, '{0}/{1}'.format(root, file))
                try:
                    with open(local_path, 'rt') as f:
                        settings[file_type].update(json.load(f))
                except json.JSONDecodeError as e:
                    log_event(level='error', status='failure', process_type='load_settings', payload=dict(error=e.args[0], filename=local_path))
                    raise e
        __settings__ = {
            k: {key: format_setting_value(value) for key, value in v.items()} for k, v in settings.items()
        }
        prefix = ''
        if settings['app'].get('environment', 'test') == 'test':
            prefix = 'test' + str(generate_random_id().split('-')[0])
        __settings__['app']['test_prefix'] = prefix
    return __settings__.get(settings_type, dict())


def format_setting_value(value):
    import json
    from .logging import log_event
    formatted_value = value
    if isinstance(value, str) and (
            any([i in value for i in ['"', '[', '{']]) or value.lower() in ['true', 'false'] or value.isdigit()):
        try:
            formatted_value = json.loads(value)
        except json.JSONDecodeError as e:
            log_event(level='debug', status='failure', process_type='load_settings',
                      payload=dict(error=e.args[0], attribute=value))
    return formatted_value
