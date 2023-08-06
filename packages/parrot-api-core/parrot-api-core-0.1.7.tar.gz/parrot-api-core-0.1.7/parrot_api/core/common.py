def generate_random_id():
    """Generate a random id

    :return: a unique UUID4 formatted string
    """
    import uuid
    return str(uuid.uuid4())


def generate_hash_id(data):
    """Generate a consistent uuid for a given input

    :return: a UUID4 formatted string
    """
    import json
    import uuid
    import hashlib
    hash_id = uuid.UUID(
        hashlib.md5(
            str(json.dumps(data, sort_keys=True)).encode('utf-8')
        ).hexdigest()
    )
    return str(hash_id)


def get_subpackage_paths():
    import parrot_api
    import pkgutil
    import os
    for finder, modname, ispkg in pkgutil.iter_modules(parrot_api.__path__):
        subpackage_path = os.path.join(finder.path, modname)
        yield subpackage_path
