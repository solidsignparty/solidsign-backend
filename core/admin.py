from django.contrib import admin

from .models import Artist, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin[Event]):
    list_display = ('__str__', 'start_time', 'location')
    search_fields = ('title', 'location')
    date_hierarchy = 'start_time'
    ordering = ('-start_time',)
    readonly_fields = ('uuid',)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin[Artist]):
    list_display = ('__str__',)
    search_fields = ('nickname',)
    ordering = ('-nickname',)
