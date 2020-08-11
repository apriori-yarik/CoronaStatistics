from django.urls import path
from coronastats.views import home_view

urlpatterns = [
    path('', home_view, name='home')
]
