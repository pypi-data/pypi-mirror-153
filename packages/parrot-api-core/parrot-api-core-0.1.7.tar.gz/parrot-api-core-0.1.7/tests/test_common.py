import pytest


def test_unique_id():
    from parrot_api.core import generate_random_id
    assert generate_random_id() != generate_random_id()


def test_random_id_is_uuid():
    from parrot_api.core import generate_random_id
    import uuid
    assert uuid.UUID(generate_random_id())


@pytest.mark.parametrize("test_input,expected",
                         [(['1', 2, '3'], 'cc209c79-020c-f993-5f78-e1a40d97b6a6'),
                          (12, 'c20ad4d7-6fe9-7759-aa27-a0c99bff6710'),
                          (dict(a=1), '42b7b4f2-9217-88ea-14da-c5566e6f06d0')])
def test_hash_id_is_uuid(test_input, expected):
    from parrot_api.core import generate_hash_id
    import uuid
    hash_id = generate_hash_id(test_input)
    assert uuid.UUID(hash_id)
    assert hash_id == expected
