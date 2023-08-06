def test_override_test_settings(test_directory):
    import os
    from parrot_api.core.settings import get_settings
    settings_dir = os.path.join(
        test_directory,
        'mocks/test_settings/')
    print(settings_dir)
    app_settings = get_settings(
        env_folder=settings_dir, refresh=True)
    assert app_settings['environment'] == 'test'
    assert app_settings['service_name'] == 'example'


def test_non_app_settings():
    from parrot_api.core.settings import get_settings
    assert get_settings(settings_type='celery')['task_always_eager']


def test_settings_parser_raises_error(test_directory):
    import os
    import pytest
    from json import JSONDecodeError
    from parrot_api.core.settings import get_settings
    settings_dir = os.path.join(
        test_directory,
        'mocks/invalid_settings/')
    print(settings_dir)
    with pytest.raises(JSONDecodeError):
        get_settings(
            env_folder=settings_dir, refresh=True)


def test_settings_loads_sub_objects(test_directory):
    import os
    from parrot_api.core.settings import get_settings
    settings_dir = os.path.join(
        test_directory,
        'mocks/stringified_settings/')
    print(settings_dir)
    app_settings = get_settings(
        env_folder=settings_dir, refresh=True)
    assert isinstance(app_settings['sub_object'], dict)
    assert app_settings['sub_object'] == dict(sub_a=1)
    assert isinstance(app_settings['sub_array'], list)
    assert app_settings['sub_array'] == ['sub_a', 1]
    assert app_settings['boolean_true'] is True
    assert app_settings['boolean_false'] is False
    assert app_settings['numeric'] == 1


def test_load_json_object():
    from parrot_api.core.settings import format_setting_value
    assert format_setting_value('{"test":"value"}') == dict(test='value')


def test_load_json_array():
    from parrot_api.core.settings import format_setting_value
    assert format_setting_value('["test", "value"]') == ['test', 'value']


def test_load_json_string():
    from parrot_api.core.settings import format_setting_value
    assert format_setting_value('"test"') == "test"


def test_load_non_json_string():
    from parrot_api.core.settings import format_setting_value
    assert format_setting_value('"test') == '"test'
