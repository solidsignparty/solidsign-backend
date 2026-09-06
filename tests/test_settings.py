import os
import subprocess
import sys


def test_prod_staticfiles_storage_uses_public_static_url() -> None:
    env = {
        **os.environ,
        'DJANGO_SETTINGS_MODULE': 'backend.settings',
        'ENV': 'prod',
        'SECRET_KEY': 'django-top-secret',
        'S3_CLIENT_ID': '',
        'S3_CLIENT_SECRET': '',
    }
    script = """
from django.contrib.staticfiles.storage import staticfiles_storage

print(staticfiles_storage.url('logo.png'))
"""

    result = subprocess.run([sys.executable, '-c', script], check=True, capture_output=True, env=env, text=True)

    assert result.stdout.strip() == 'https://d8a8e64a-33f0-4b13-953b-862c08b5c7be.selstorage.ru/logo.png'
