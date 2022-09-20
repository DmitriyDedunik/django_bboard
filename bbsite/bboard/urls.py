"""Describe project urls."""
from django.contrib.auth.decorators import login_required
from django.urls import path
from bboard import views

app_name = 'bboard'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'create/',
        login_required(views.BbCreateView.as_view(), login_url='/login/'),
        name='create',
    ),
    path('create_new/', views.BbCreateView_new, name='create_new'),
    path('by_rubric/<int:rubric_id>/', views.by_rubric, name='by_rubric'),
    path('rubrics/', views.rubrics, name='rubrics'),
    path('create_rubric/', views.RubricCreate.as_view(), name='create_rubric'),
    path('create_city/', views.CityCreateView.as_view(), name='create_city'),
    path(
        'create/<int:pk>/update/',
        views.NewUpdate.as_view(),
        name='new_update',
    ),
    path('detail/<int:pk>/', views.BbDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.BbDeleteView.as_view(), name='delete'),
    path('registration/', views.Registration.as_view(), name='registration'),
    path('my_bb/', views.my_bb, name='my_bb'),
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('send_message/<int:bb_id>/<int:user_id>/', views.send_message, name='send_message'),
    path('chats/', views.chats, name='chats'),
    path('yandex_response/', views.yandex_response, name='yandex_response'),
    path('google_response/', views.google_response, name='google_response'),
]
