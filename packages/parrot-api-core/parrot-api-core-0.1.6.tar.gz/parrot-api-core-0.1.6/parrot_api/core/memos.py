from parrot_api.core import generate_hash_id
from parrot_api.core import log_event

memos = dict()


def set_memo(namespace, value, args=None, kwargs=None, log_inputs=True, log_value=True):
    global memos

    hash_id = generate_hash_id(dict(args=args, kwargs=kwargs))
    if namespace not in memos.keys():
        memos[namespace] = dict()
    memos[namespace][hash_id] = dict(args=args, kwargs=kwargs, value=value)
    log_payload = dict(namespace=namespace, key=hash_id)
    if log_inputs:
        log_payload['args'] = args
        log_payload['kwargs'] = kwargs
    if log_value:
        log_payload['value'] = value
    log_event(level='debug', status='success', process_type='set_memo',
              payload=log_payload)
    return value


def get_memo(namespace, args=None, kwargs=None, log_inputs=True, log_value=True):
    global memos

    hash_id = generate_hash_id(dict(args=args, kwargs=kwargs))
    value = memos.get(namespace, dict()).get(hash_id, dict()).get('value')
    log_payload = dict(namespace=namespace, key=hash_id)
    if log_inputs:
        log_payload['args'] = args
        log_payload['kwargs'] = kwargs
    if log_value:
        log_payload['value'] = value
    log_event(level='debug', status='success', process_type='get_memo',
              payload=log_payload)
    return value
