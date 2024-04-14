from datetime import datetime
from typing import TypedDict

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Event


class EventDict(TypedDict):
    title: str
    start_time: datetime
    end_time: datetime
    location: str
    tickets_url: str
    image_url: str


@require_http_methods(['GET'])
def events(request: HttpRequest) -> JsonResponse:
    items: list[EventDict] = []
    for event in Event.objects.all().order_by('-start_time'):
        items.append(
            {
                'title': event.title,
                'start_time': event.start_time,
                'end_time': event.end_time,
                'location': event.location,
                'tickets_url': event.tickets_url,
                'image_url': event.image_url.url,
            }
        )
    return JsonResponse(items, safe=False)
