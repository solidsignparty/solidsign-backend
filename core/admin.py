from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'start_time', 'location')
    search_fields = ('title', 'location')
    date_hierarchy = 'start_time'
    ordering = ('-start_time',)
