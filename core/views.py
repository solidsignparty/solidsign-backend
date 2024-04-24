from datetime import datetime
from io import BytesIO
from typing import Any, TypedDict
from urllib.parse import urlencode

from django.http import FileResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from core.models import ICS_DATE_FORMAT, Artist, Event

from .context_processors import PageEnum


class EventListView(ListView[Event]):
    template_name = 'core/includes/events.html'
    model = Event
    context_object_name = 'events'
    ordering = ('-start_time',)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        events_list = context['object_list'] or []
        if latest_event := events_list[0] if len(events_list) > 0 else None:
            context['meta'] = latest_event.as_meta(self.request)
        return context


class IndexView(EventListView):
    paginate_by = 3
    template_name = 'core/index.html'
    extra_context = {'page': PageEnum.EVENTS}


class ArtistListView(ListView[Artist]):
    model = Artist
    template_name = 'core/artists.html'
    extra_context = {'page': PageEnum.ARTISTS}
    ordering = ('nickname',)
    context_object_name = 'artists'


def _ics_calendar(event: Event) -> FileResponse:
    timestamp = timezone.now()
    content = loader.render_to_string(
        'core/calendar/ics.tmpl',
        {
            'event': event,
            'timestmp': f'{timestamp.strftime(ICS_DATE_FORMAT)}Z',
            'uuid': event.uuid,
        },
    )
    return FileResponse(BytesIO(content.encode('utf-8')), filename='calendar.ics')


def _google_calendar(event: Event) -> HttpResponseRedirect:
    params = {
        'action': 'TEMPLATE',
        'dates': f'{event.start_time_formatted}Z/{event.end_time_formatted}Z',
        'text': event.title,
        'location': event.location,
    }
    return HttpResponseRedirect(f'https://calendar.google.com/calendar/render?{urlencode(params)}')


def calendar(request: HttpRequest, event_id: int) -> FileResponse | HttpResponseRedirect:
    event = get_object_or_404(Event, pk=event_id)
    if 'Mac' in request.headers.get('user-agent', ''):
        return _ics_calendar(event)
    return _google_calendar(event)


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
                'image_url': event.image.url,
            }
        )
    return JsonResponse(items, safe=False)
