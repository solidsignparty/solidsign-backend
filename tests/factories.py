import datetime
from typing import Callable, Protocol, cast

import factory
from faker import Factory


class FakerAdapter(Protocol):
    company: Callable[[], str]
    address: Callable[[], str]
    date_time: Callable[[datetime.tzinfo], datetime.datetime]
    url: Callable[[], str]


faker = cast(FakerAdapter, Factory.create())


class EventFactory(factory.django.DjangoModelFactory):  # type: ignore[misc]
    title = faker.company()
    location = faker.address()
    start_time = faker.date_time(datetime.UTC)
    end_time = factory.LazyAttribute(lambda event: event.start_time + datetime.timedelta(hours=8))
    image_url = factory.django.ImageField()
    tickets_url = faker.url()

    class Meta:
        model = 'core.Event'
        django_get_or_create = ('title',)
