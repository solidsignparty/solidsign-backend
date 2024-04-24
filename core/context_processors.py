from enum import StrEnum
from typing import TypedDict

from django.http import HttpRequest
from django.urls import reverse_lazy


class PageEnum(StrEnum):
    EVENTS = 'events'
    ARTISTS = 'artists'


class MenuItem(TypedDict):
    page: PageEnum
    href: str
    title: str


MENU_ITEMS = [
    {'page': PageEnum.EVENTS, 'title': 'События', 'href': reverse_lazy('index')},
    {'page': PageEnum.ARTISTS, 'title': 'Артисты', 'href': reverse_lazy('artists')},
]


def menu(request: HttpRequest) -> dict[str, list[dict[str, str]]]:
    return {'menu_items': MENU_ITEMS}
