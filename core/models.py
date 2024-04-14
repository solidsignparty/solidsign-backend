import datetime

from django.db import models
from django.utils import timezone


def default_start_time() -> datetime.datetime:
    return datetime.datetime.combine(timezone.now(), datetime.time(19, 0), datetime.UTC)


def default_end_time() -> datetime.datetime:
    return datetime.datetime.combine(timezone.now(), datetime.time(2, 0), datetime.UTC)


class Event(models.Model):
    start_time = models.DateTimeField(verbose_name='Время начала', default=default_start_time)
    end_time = models.DateTimeField(verbose_name='Время окончания', default=default_end_time)
    title = models.CharField(max_length=256, verbose_name='Название')
    location = models.CharField(max_length=256, verbose_name='Локация')
    tickets_url = models.URLField(verbose_name='Ссылка на билеты')
    image_url = models.ImageField(upload_to='events/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Мероприятиe'
        verbose_name_plural = 'Мероприятия'

    def __str__(self) -> str:
        return f'[{self.start_time.date()}] {self.title}'
