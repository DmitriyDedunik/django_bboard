from venv import create
from django.urls import path
from .views import RubricCreate, index, BbCreateView, BbCreateView_new, by_rubric, rubrics, NewUpdate, BbDetailView, BbDeleteView, CityCreateView

app_name = 'bboard'

urlpatterns = [
    path('', index, name='index'),
    path('create/', BbCreateView.as_view(), name='create'),
    path('create_new/', BbCreateView_new, name='create_new'),
    path('by_rubric/<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('rubrics/', rubrics, name='rubrics'),
    path('create_rubric/', RubricCreate.as_view(), name='create_rubric'),
    path('create_city/', CityCreateView.as_view(), name='create_city'),
    path('create/<int:pk>/update/', NewUpdate.as_view(), name='new_update'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
]
