from venv import create
from django.urls import path
from .views import index, BbCreateView, BbCreateView_new, by_rubric

app_name = 'bbsite_app'

urlpatterns = [
    path('', index, name='index'),
    path('create/', BbCreateView.as_view(), name='create'),
    path('create_new/', BbCreateView_new, name='create_new'),
    path('by_rubric/<int:rubric_id>/', by_rubric, name='by_rubric'),
]
