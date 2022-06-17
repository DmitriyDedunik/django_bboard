from venv import create
from django.urls import path
from .views import index, BbCreateView

urlpatterns = [
    path('', index, name='index'),
    path('create/', BbCreateView.as_view(), name='create'),
]
