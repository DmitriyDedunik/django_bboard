from venv import create
from django.urls import path
from .views import RubricCreate, index, BbCreateView, BbCreateView_new, by_rubric, rubrics, New_update

app_name = 'bbsite_app'

urlpatterns = [
    path('', index, name='index'),
    path('create/', BbCreateView.as_view(), name='create'),
    path('create_new/', BbCreateView_new, name='create_new'),
    path('by_rubric/<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('rubrics/', rubrics, name='rubrics'),
    path('create_rubric/', RubricCreate.as_view(), name='create_rubric'),
    path('create/<int:new_id>/update/', New_update.as_view(), name='new_update'),
]
