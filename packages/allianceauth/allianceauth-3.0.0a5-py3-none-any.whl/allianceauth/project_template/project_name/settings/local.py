# Every setting in base.py can be overloaded by redefining it here.
from .base import *

# These are required for Django to function properly. Don't touch.
ROOT_URLCONF = '{{ project_name }}.urls'
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'
SECRET_KEY = '{{ secret_key }}'

# This is where css/images will be placed for your webserver to read
STATIC_ROOT = "/var/www/{{ project_name }}/static/"

# Change this to change the name of the auth site displayed
# in page titles and the site header.
SITE_NAME = '{{ project_name }}'

# Change this to enable/disable debug mode, which displays
# useful error messages but can leak sensitive data.
DEBUG = False

# Add any additional apps to this list.
INSTALLED_APPS += [

]

# To change the logging level for extensions, uncomment the following line.
# LOGGING['handlers']['extension_file']['level'] = 'DEBUG'


# Enter credentials to use MySQL/MariaDB. Comment out to use sqlite3
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'alliance_auth',
    'USER': '',
    'PASSWORD': '',
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'OPTIONS': {'charset': 'utf8mb4'},
}

# Register an application at https://developers.eveonline.com for Authentication
# & API Access and fill out these settings. Be sure to set the callback URL
# to https://example.com/sso/callback substituting your domain for example.com
# Logging in to auth requires the publicData scope (can be overridden through the
# LOGIN_TOKEN_SCOPES setting). Other apps may require more (see their docs).
ESI_SSO_CLIENT_ID = ''
ESI_SSO_CLIENT_SECRET = ''
ESI_SSO_CALLBACK_URL = ''
ESI_USER_CONTACT_EMAIL = ''    # A server maintainer that CCP can contact in case of issues.

# By default emails are validated before new users can log in.
# It's recommended to use a free service like SparkPost or Elastic Email to send email.
# https://www.sparkpost.com/docs/integrations/django/
# https://elasticemail.com/resources/settings/smtp-api/
# Set the default from email to something like 'noreply@example.com'
# Email validation can be turned off by uncommenting the line below. This can break some services.
# REGISTRATION_VERIFY_EMAIL = False
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = ''

# Cache compression can help on bigger auths where ram starts to become an issue.
# Uncomment the following 3 lines to enable.

#CACHES["default"]["OPTIONS"] = {
#    "COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",
#}

#######################################
# Add any custom settings below here. #
#######################################
