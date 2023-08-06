# import pytest
# from aioresponses import aioresponses
#
#
# def add_default_mocks(responses, app_settings):
#     return responses
#
#
# @pytest.fixture(scope='session')
# def event_loop():
#     import asyncio
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
#
#
# @pytest.fixture
# def mock_aioresponse(app_settings):
#     responses = aioresponses(passthrough=['http://127.0.0.1'])
#     return responses
#
#
# @pytest.fixture()
# async def async_client(aiohttp_client, test_directory):
#     import os
#     from parrot_api.core.server import create_server
#     app = create_server(spec_dir=os.path.join(test_directory, 'mocks/schemas'), sync=False)
#     return await aiohttp_client(app.app)
#
#
# async def test_valid_token(async_client, mock_aioresponse, valid_access_headers, public_keys, app_settings):
#     with mock_aioresponse as mocked:
#         mocked.add(method='get', url=app_settings['auth_keys_url'], payload=public_keys)
#         resp = await async_client.get('/v1/async/hello', headers=valid_access_headers)
#         assert resp.status == 200
#
#
# async def test_invalid_token(async_client, mock_aioresponse, invalid_access_headers, public_keys, app_settings):
#     with mock_aioresponse as mocked:
#         mocked.add(method='get', url=app_settings['auth_keys_url'], payload=public_keys)
#         resp = await async_client.get('/v1/async/hello', headers=invalid_access_headers)
#         assert resp.status == 401
#
#
# async def test_unauthorized_token(async_client, mock_aioresponse, unauthorized_access_headers, public_keys, app_settings):
#     with mock_aioresponse as mocked:
#         mocked.add(method='get', url=app_settings['auth_keys_url'], payload=public_keys)
#         resp = await async_client.get('/v1/async/hello', headers=unauthorized_access_headers)
#         assert resp.status == 403
