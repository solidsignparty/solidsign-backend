from datetime import datetime
from typing import Callable
from urllib.parse import parse_qsl, urlparse

import pytest
from django.test import Client
from django.urls import reverse, reverse_lazy

from core.models import Artist, Event

pytestmark = pytest.mark.django_db


def format_time(timestamp: datetime) -> str:
    return timestamp.strftime('%d.%m.%Y')


@pytest.fixture
def assert_upcoming_event() -> Callable[[Event, str], None]:
    def _assert_upcoming_event(event: Event, content: str) -> None:
        for item in [
            format_time(event.start_time),
            event.tickets_url,
            event.image.url,
            'Купить билет',
            'Не забыть',
            'Следующее мероприятие',
        ]:
            assert item in content

    return _assert_upcoming_event


@pytest.fixture
def assert_past_event() -> Callable[[Event, str], None]:
    def _assert_past_event(event: Event, content: str) -> None:
        for item in [
            format_time(event.start_time),
            event.image.url,
        ]:
            assert item in content
        for item in [
            event.tickets_url,
            'Купить билет',
            'Не забыть',
            'Следующее мероприятие',
        ]:
            assert item not in content

    return _assert_past_event


@pytest.mark.parametrize('event', [{'past_due': False}], indirect=True)
@pytest.mark.parametrize('url', [reverse_lazy('events'), reverse_lazy('index')])
def test_upcoming_event(
    client: Client, event: Event, assert_upcoming_event: Callable[[Event, str], None], url: str
) -> None:
    response = client.get(url)
    assert response.status_code == 200
    assert_upcoming_event(event, response.content.decode())


@pytest.mark.parametrize('event', [{'past_due': True}], indirect=True)
@pytest.mark.parametrize('url', [reverse_lazy('events'), reverse_lazy('index')])
def test_past_event(
    client: Client,
    event: Event,
    assert_past_event: Callable[[Event, str], None],
    url: str,
) -> None:
    response = client.get(url)
    assert response.status_code == 200
    assert_past_event(event, response.content.decode())


@pytest.fixture
def mac_user_agent() -> str:
    return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'  # noqa


@pytest.fixture
def linux_user_agent() -> str:
    return 'Mozilla/5.0 (X11; U; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/124.0.6275.209 Chrome/124.0.6275.209 Safari/537.36'  # noqa


def test_calendar_ics(event: Event, client: Client, mac_user_agent: str) -> None:
    response = client.get(reverse('calendar', kwargs={'event_id': event.pk}), headers={'User-Agent': mac_user_agent})
    assert response.status_code == 200
    assert hasattr(response, 'streaming_content')
    assert len(list(response.streaming_content)) > 0


def test_calendar_google(event: Event, client: Client, linux_user_agent: str) -> None:
    response = client.get(reverse('calendar', kwargs={'event_id': event.pk}), headers={'User-Agent': linux_user_agent})
    assert response.status_code == 302
    urlparts = urlparse(response.headers['location'])
    assert urlparts.scheme == 'https'
    assert urlparts.netloc == 'calendar.google.com'
    assert urlparts.path == '/calendar/render'
    query = dict(parse_qsl(urlparts.query))
    assert query == {
        'action': 'TEMPLATE',
        'dates': f'{event.start_time_formatted}Z/{event.end_time_formatted}Z',
        'text': event.title,
        'location': event.location,
    }


def test_artists(artist: Artist, client: Client) -> None:
    response = client.get(reverse('artists'))
    assert response.status_code == 200
    assert artist.nickname in response.content.decode()
    assert artist.photo.url in response.content.decode()
