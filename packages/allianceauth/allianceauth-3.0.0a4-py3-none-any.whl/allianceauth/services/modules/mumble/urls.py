from django.conf.urls import include
from django.urls import path

from . import views

app_name = 'mumble'

module_urls = [
    # Mumble service control
    path('activate/', views.CreateAccountMumbleView.as_view(), name='activate'),
    path('deactivate/', views.DeleteMumbleView.as_view(), name='deactivate'),
    path('reset_password/', views.ResetPasswordMumbleView.as_view(), name='reset_password'),
    path('set_password/', views.SetPasswordMumbleView.as_view(), name='set_password'),
]

urlpatterns = [
    path('mumble/', include((module_urls, app_name), namespace=app_name))
]
