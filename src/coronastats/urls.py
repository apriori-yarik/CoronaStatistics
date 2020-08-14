from django.urls import path
from coronastats.views import home_view, stats_by_country_view, world_view

urlpatterns = [
    path('', home_view, name='home'),
    path('stats-by-country/', stats_by_country_view, name='stats-by-country'),
    path('world/', world_view, name='world')
]
