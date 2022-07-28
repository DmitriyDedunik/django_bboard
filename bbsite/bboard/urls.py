"""Describe project urls."""
from django.urls import path, include

from bboard import views

app_name = 'bboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.BbCreateView.as_view(), name='create'),
    path('create_new/', views.BbCreateView_new, name='create_new'),
    path('by_rubric/<int:rubric_id>/', views.by_rubric, name='by_rubric'),
    path('rubrics/', views.rubrics, name='rubrics'),
    path('create_rubric/', views.RubricCreate.as_view(), name='create_rubric'),
    path('create_city/', views.CityCreateView.as_view(), name='create_city'),
    path('create/<int:pk>/update/', views.NewUpdate.as_view(), name='new_update'),
    path('detail/<int:pk>/', views.BbDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.BbDeleteView.as_view(), name='delete'),
    path('registration/', views.Registration.as_view(), name='registration'),
    path('', include('django.contrib.auth.urls')),
    path('my_bb/', views.My_Bb, name='my_bb'),
]
