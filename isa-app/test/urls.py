from django.urls import path

from isa-app import home

urlpatterns = [
    path('', home.index, name='index'),
]

