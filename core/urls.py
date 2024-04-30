from django.urls import path

from . import views

urlpatterns = [
    path('_parts/events/', views.EventListView.as_view(), name='events'),
    path('event/<int:event_id>/calendar/', views.calendar, name='calendar'),
    path('artists/', views.ArtistListView.as_view(), name='artists'),
    path('', views.IndexView.as_view(), name='index'),
]
