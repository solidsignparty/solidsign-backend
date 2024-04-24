import os
import re
from datetime import UTC, datetime
from io import BytesIO

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse
from PIL import Image

from core.models import Artist, Event

pytestmark = pytest.mark.django_db


@pytest.fixture
def add_event_url() -> str:
    return reverse('admin:core_event_add')


@pytest.fixture
def list_events_url() -> str:
    return reverse('admin:core_event_changelist')


@pytest.fixture
def image() -> SimpleUploadedFile:
    img = Image.new('RGB', (100, 100))
    buf = BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0, os.SEEK_SET)
    return SimpleUploadedFile('image.jpg', buf.getvalue(), content_type='image/jpeg')


def test_can_view_add_event_page(admin_client: Client, add_event_url: str) -> None:
    response = admin_client.get(add_event_url)
    assert response.status_code == 200


def test_can_view_change_event_page(admin_client: Client, event: Event) -> None:
    url = reverse('admin:core_event_change', kwargs={'object_id': event.pk})
    response = admin_client.get(url)
    assert response.status_code == 200


def test_can_search_event(admin_client: Client, event: Event, list_events_url: str) -> None:
    response = admin_client.get(list_events_url + '?q=SOLID')
    assert response.status_code == 200


def test_can_create_event(
    admin_client: Client,
    add_event_url: str,
    list_events_url: str,
    image: SimpleUploadedFile,
) -> None:
    assert not Event.objects.exists()
    start_time = datetime(2024, 4, 27, 19, tzinfo=UTC)
    end_time = datetime(2024, 4, 28, 2, tzinfo=UTC)
    title = 'Solid Sign Shift #2'
    location = 'Dark Size'
    tickets_url = 'https://buy-tickets.org'
    response = admin_client.post(
        add_event_url,
        {
            'start_time_0': start_time.strftime('%d.%m.%Y'),
            'start_time_1': start_time.strftime('22:00'),
            'end_time_0': end_time.strftime('%d.%m.%Y'),
            'end_time_1': end_time.strftime('05:00'),
            'title': title,
            'location': location,
            'tickets_url': tickets_url,
            'image': image,
        },
    )
    assert response.status_code == 302
    assert response.headers['location'] == list_events_url
    event = Event.objects.get()
    assert event.start_time == start_time
    assert event.end_time == end_time
    assert event.title == title
    assert event.location == location
    assert event.tickets_url == tickets_url
    assert re.match(r'/events/.*\.jpg', event.image.url)


def test_can_view_change_artist_page(admin_client: Client, artist: Artist) -> None:
    url = reverse('admin:core_artist_change', kwargs={'object_id': artist.pk})
    response = admin_client.get(url)
    assert response.status_code == 200


@pytest.fixture
def add_artist_url() -> str:
    return reverse('admin:core_artist_add')


@pytest.fixture
def list_artists_url() -> str:
    return reverse('admin:core_artist_changelist')


def test_can_search_artist(admin_client: Client, artist: Artist, list_artists_url: str) -> None:
    response = admin_client.get(list_artists_url + '?q=AKINOV')
    assert response.status_code == 200


def test_can_view_add_artist_page(admin_client: Client, add_artist_url: str) -> None:
    response = admin_client.get(add_artist_url)
    assert response.status_code == 200


def test_can_create_artist(
    admin_client: Client,
    add_artist_url: str,
    list_artists_url: str,
    image: SimpleUploadedFile,
) -> None:
    response = admin_client.post(
        add_artist_url,
        {
            'nickname': 'John Doe',
            'photo': image,
        },
    )
    assert response.status_code == 302
    assert response.headers['location'] == list_artists_url
