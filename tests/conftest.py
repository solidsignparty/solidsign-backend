from datetime import timedelta
from shutil import rmtree
from typing import Generator, cast

import pytest
from django.conf import settings
from django.utils import timezone

from core.models import Artist, Event

from .factories import ArtistFactory, EventFactory

NOT_SET = object()


@pytest.fixture
def event(request: pytest.FixtureRequest) -> Event:
    past_due = getattr(request, 'param', {}).get('past_due')
    match past_due:
        case True:
            event = EventFactory.create(start_time=timezone.now() - timedelta(days=1))
        case False:
            event = EventFactory.create(start_time=timezone.now() + timedelta(days=1))
        case _:
            event = EventFactory.create()
    return cast(Event, event)


@pytest.fixture(scope='session', autouse=True)
def clean_static_storage() -> Generator[None, None, None]:
    try:
        yield
    finally:
        rmtree(settings.BASE_DIR / 'events', ignore_errors=True)
        rmtree(settings.BASE_DIR / 'artists', ignore_errors=True)


@pytest.fixture
def artist() -> Artist:
    return cast(Artist, ArtistFactory.create())
