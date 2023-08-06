LOGGER = None
DEFAULT_ATTRIBUTES = None


def configure_default_log_attributes(attributes: dict):
    global DEFAULT_ATTRIBUTES
    DEFAULT_ATTRIBUTES = attributes if isinstance(attributes, dict) else dict()
    return DEFAULT_ATTRIBUTES


def get_logger():
    import logging, sys
    import os
    import json
    import logging.config
    global LOGGER
    if LOGGER is None:
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        if os.getenv('LOGGING_CONFIG_PATH'):
            with open(os.getenv('LOGGER_CONFIG_PATH'), 'rt', encoding='utf-8') as f:
                config = json.load(f)
            logging.config.dictConfig(config=config)
        else:
            logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        LOGGER = logging.getLogger()
    return LOGGER


def log_event(level: str, status: str, process_type: str, payload: dict):
    import json
    assert isinstance(payload, dict)
    assert status in {'success', 'anomalous', 'failure', 're-queued'}
    global DEFAULT_ATTRIBUTES
    attributes = DEFAULT_ATTRIBUTES if DEFAULT_ATTRIBUTES is not None else dict()
    level_mapping = dict(
        critical=50,
        error=40,
        warning=30,
        info=20,
        debug=10
    )
    log_message = {
        "process_type": process_type,
        "status": status,
        "payload": payload,
        **attributes
    }
    get_logger().log(level=level_mapping[level.lower()], msg=json.dumps(log_message))
    return log_message
