from django.urls import path
import esi.urls

from django.conf.urls import include
from django.contrib import admin
from django.views.generic.base import TemplateView

import allianceauth.authentication.views
import allianceauth.authentication.urls
import allianceauth.notifications.urls
import allianceauth.groupmanagement.urls
import allianceauth.services.urls
from allianceauth.authentication.decorators import main_character_required, decorate_url_patterns
from allianceauth import NAME
from allianceauth import views
from allianceauth.authentication import hmac_urls
from allianceauth.hooks import get_hooks

admin.site.site_header = NAME


# Functional/Untranslated URL's
urlpatterns = [
    # Locale
    path('i18n/', include('django.conf.urls.i18n')),

    # Authentication
    path('', include(allianceauth.authentication.urls)),
    path('account/login/', TemplateView.as_view(template_name='public/login.html'), name='auth_login_user'),
    path('account/', include(hmac_urls)),

    # Admin urls
    path('admin/', admin.site.urls),

    # SSO
    path('sso/', include((esi.urls, 'esi'), namespace='esi')),
    path('sso/login', allianceauth.authentication.views.sso_login, name='auth_sso_login'),

    # Notifications
    path('', include(allianceauth.notifications.urls)),

    # Groups
    path('', include(allianceauth.groupmanagement.urls)),

    # Services
    path('', decorate_url_patterns(allianceauth.services.urls.urlpatterns, main_character_required)),

    # Night mode
    path('night/', views.NightModeRedirectView.as_view(), name='nightmode')
]


# Append app urls
app_urls = get_hooks('url_hook')
for app in app_urls:
    urlpatterns += [path('', decorate_url_patterns([app().include_pattern], main_character_required))]
