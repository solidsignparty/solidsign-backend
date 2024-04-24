import datetime
import uuid

from django.db import models
from django.utils import timezone
from meta.models import ModelMeta


def default_start_time() -> datetime.datetime:
    return datetime.datetime.combine(timezone.now(), datetime.time(19, 0), datetime.UTC)


def default_end_time() -> datetime.datetime:
    return datetime.datetime.combine(timezone.now(), datetime.time(2, 0), datetime.UTC)


ICS_DATE_FORMAT = '%Y%m%dT%H%M%S'


class Event(ModelMeta, models.Model):  # type: ignore[misc]
    start_time = models.DateTimeField(verbose_name='Время начала', default=default_start_time)
    end_time = models.DateTimeField(verbose_name='Время окончания', default=default_end_time)
    title = models.CharField(max_length=256, verbose_name='Название')
    location = models.CharField(max_length=256, verbose_name='Локация')
    tickets_url = models.URLField(verbose_name='Ссылка на билеты')
    image = models.ImageField(upload_to='events/', verbose_name='Изображение')
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name='Идентификатор для каледнаря')
    description = models.TextField(verbose_name='Описание', blank=True, default='')

    _metadata = {
        'title': 'title',
        'description': 'description',
        'image': 'get_meta_image',
    }

    class Meta:
        verbose_name = 'Мероприятиe'
        verbose_name_plural = 'Мероприятия'

    def __str__(self) -> str:
        return f'[{self.start_time.date()}] {self.title}'

    @property
    def is_past_due(self) -> bool:
        return self.start_time <= timezone.now()

    @property
    def start_time_formatted(self) -> str:
        return self.start_time.strftime(ICS_DATE_FORMAT)

    @property
    def end_time_formatted(self) -> str:
        return self.end_time.strftime(ICS_DATE_FORMAT)

    def get_meta_image(self) -> str:
        return str(self.image.url)

    def get_meta_description(self) -> str:
        return self.description or self.title


class Artist(models.Model):
    nickname = models.CharField(verbose_name='Никнейм', max_length=128, unique=True)
    photo = models.ImageField(upload_to='artists/', verbose_name='Фото')

    class Meta:
        verbose_name = 'Артист'
        verbose_name_plural = 'Артисты'

    def __str__(self) -> str:
        return self.nickname
