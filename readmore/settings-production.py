"""
Django settings for readmore project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = '/app/staticfiles'
STATIC_URL = '/static/'


ADMINS = (
    ('Sander', 'sander@perceptum.nl'),
    ('Robrecht', 'robrecht@perceptum.nl'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nam+hzdm-pw7$l5y$k+yk)xfhm*1nmy2v!^d$7&yp29n%t8@y!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = (
    'django.contrib.admin',
    'polymorphic',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'longerusernameandemail',
    'django_summernote',
    'main',
    'cover',
    'content',
    'teacher',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.windowslive',
    'allauth.socialaccount.providers.google',
	'compressor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

LANGUAGE_CODE = 'nl'
LANGUAGES = (
  ('nl', ('Dutch')),
)

ROOT_URLCONF = 'readmore.urls'

WSGI_APPLICATION = 'readmore.wsgi.application'

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {'default': dj_database_url.config()}

# Authentication back-end
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

# auth and allauth settings
# Settings for social providers
# Note: Windows Live requires no settings
LOGIN_REDIRECT_URL = '/dashboard'
ACCOUNT_EMAIL_REQUIRED = 'True'
SOCIALACCOUNT_EMAIL_REQUIRED = 'True'
SOCIALACCOUNT_AUTO_SIGNUP = 'True'
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = 'False'
AUTH_PROFILE_MODULE = 'main.UserProfile'
SIGNUP_ENABLED = True
ACCOUNT_FORMS = {'signup': 'main.forms.ReadMoreSignupForm'}
ACCOUNT_ADAPTER = "main.adapter.ReadMoreAccountAdapter"

SOCIALACCOUNT_PROVIDERS = \
    { 'google':
        { 'SCOPE': ['profile', 'email'],
          'AUTH_PARAMS': { 'access_type': 'online' } }}

REQUIRE_UNIQUE_EMAIL = False

# Template Context
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Wikipedia source

LOCALE_PATHS = (os.path.join(os.path.dirname(BASE_DIR), 'locale'),)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'collectstatic'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': True,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Change editor size
    'width': '100%',
    'height': '450',

    # Set editor language/locale
    'lang': 'en-US',
}

# Mediawiki content settings
CONTENT_MEDIAWIKI_LANG = "nl"

import os
EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
EMAIL_HOST= 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
SERVER_EMAIL = 'readmore-platform@perceptum.nl'
