def test_log_format():
    from parrot_api.core import log_event
    log_event(
        level='error', status='failure', process_type='delivery', payload={'message': 'test'}
    )
