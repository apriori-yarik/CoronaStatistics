from django.urls import path
from coronastats.views import home_view, stats_by_country_view, world_view, country_view, predictions_forms_view, predictions_view

urlpatterns = [
    path('', home_view, name='home'),
    path('stats-by-country/', stats_by_country_view, name='stats-by-country'),
    path('stats-by-country/<str:name>', country_view, name='country'),
    path('world/', world_view, name='world'),
    path('predictions/', predictions_forms_view, name='predictions-form'),
    path('predictions/<str:name>', predictions_view, name='predictions')
]


