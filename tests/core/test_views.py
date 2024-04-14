from datetime import datetime

import pytest
from django.test import Client

from core.models import Event

pytestmark = pytest.mark.django_db


def format_time(timestamp: datetime) -> str:
    return timestamp.isoformat(timespec='milliseconds').replace('+00:00', 'Z')


def test_events(client: Client, event: Event) -> None:
    response = client.get('/events/')
    assert response.status_code == 200
    assert response.json() == [
        {
            'title': event.title,
            'start_time': format_time(event.start_time),
            'end_time': format_time(event.end_time),
            'location': event.location,
            'tickets_url': event.tickets_url,
            'image_url': event.image_url.url,
        }
    ]
