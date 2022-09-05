"""Describe project urls."""
from django.urls import path
from bb_api import views

app_name = 'bb_api'

urlpatterns = [
    path('list_bb', views.list_bb, name='list_bb'),
    path('json_test', views.json_test, name='json_test'),
    path('json_test2', views.json_test2, name='json_test2'),
]
