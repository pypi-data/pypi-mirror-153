from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'account/login/',
        TemplateView.as_view(template_name='public/login.html'),
        name='login'
    ),
    path(
        'account/characters/main/',
        views.main_character_change,
        name='change_main_character'
    ),
    path(
        'account/characters/add/',
        views.add_character,
        name='add_character'
    ),
    path('dashboard/', views.dashboard, name='dashboard'),
]
