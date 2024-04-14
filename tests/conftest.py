from shutil import rmtree
from typing import Generator, cast

import pytest
from django.conf import settings

from core.models import Event

from .factories import EventFactory


@pytest.fixture
def event() -> Event:
    return cast(Event, EventFactory.create())


@pytest.fixture(scope='session', autouse=True)
def clean_static_storage() -> Generator[None, None, None]:
    try:
        yield
    finally:
        rmtree(settings.BASE_DIR / 'events')
