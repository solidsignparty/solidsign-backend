from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = ('title', 'location')
    date_hierarchy = 'start_time'
