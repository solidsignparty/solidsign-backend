import importlib
import sys
from collections.abc import Callable, Iterator
from types import ModuleType

import pytest


@pytest.fixture
def reload_settings(monkeypatch: pytest.MonkeyPatch) -> Iterator[Callable[[dict[str, str]], ModuleType]]:
    original_settings_module = sys.modules.get('backend.settings')

    def _reload(env: dict[str, str]) -> ModuleType:
        for key in [
            'ENV',
            'SECRET_KEY',
            'S3_BUCKET_NAME',
            'S3_CLIENT_ID',
            'S3_CLIENT_SECRET',
            'S3_ENDPOINT_URL',
            'S3_REGION_NAME',
        ]:
            monkeypatch.delenv(key, raising=False)
        for key, value in env.items():
            monkeypatch.setenv(key, value)
        sys.modules.pop('backend.settings', None)
        return importlib.import_module('backend.settings')

    yield _reload
    if original_settings_module is None:
        sys.modules.pop('backend.settings', None)
    else:
        sys.modules['backend.settings'] = original_settings_module


def test_prod_s3_storage_uses_selectel_env(reload_settings: Callable[[dict[str, str]], ModuleType]) -> None:
    settings = reload_settings(
        {
            'ENV': 'prod',
            'SECRET_KEY': 'secret',
            'S3_BUCKET_NAME': 'custom-bucket',
            'S3_CLIENT_ID': 'access-key',
            'S3_CLIENT_SECRET': 'secret-key',
            'S3_ENDPOINT_URL': 'https://s3.ru-7.storage.selcloud.ru',
            'S3_REGION_NAME': 'ru-7',
        }
    )

    assert settings.STATIC_URL == 'https://s3.ru-7.storage.selcloud.ru/custom-bucket/'
    assert settings.STORAGES['staticfiles']['BACKEND'] == 'storages.backends.s3.S3Storage'
    assert settings.STORAGES['staticfiles']['OPTIONS'] == {
        'bucket_name': 'custom-bucket',
        'access_key': 'access-key',
        'secret_key': 'secret-key',
        'endpoint_url': 'https://s3.ru-7.storage.selcloud.ru',
        'region_name': 'ru-7',
        'querystring_auth': False,
    }


def test_dev_uses_local_static_and_media(reload_settings: Callable[[dict[str, str]], ModuleType]) -> None:
    settings = reload_settings({'ENV': 'dev', 'SECRET_KEY': 'secret'})

    assert settings.STATIC_URL == 'static/'
    assert settings.MEDIA_URL == 'media/'
    assert not hasattr(settings, 'STORAGES')
