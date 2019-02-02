# coding=utf-8
"""
Django settings for siw project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
import sys
from decouple import config
from unipath import Path
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# Questo è il valore di default che ho modificato come sotto per decouple.
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).parent
PROJECT_DIR = Path(__file__).parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'uk)bf8(h2cwr2ou%$@esix(%3mees*zr*@7_y=pgj@cv3@wp%p'
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
DEBUG_PRINT = config('DEBUG_PRINT', default=False, cast=bool)


ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

INTERNAL_IPS = config('INTERNAL_IPS', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'debug_toolbar',
    'widget_tweaks',
    'import_export',
    'accounts',
    'attesta',
    'amm',
    'anagrafe',
    'collaboratori',
    'corsi',
    'acquisti'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'siw.context_processor.si_middleware',
    'django_cprofile_middleware.middleware.ProfilerMiddleware',
]

ROOT_URLCONF = 'siw.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_DIR.parent.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'siw.context_processor.si_special_dicts',
            ],
        },
    },
]

WSGI_APPLICATION = 'siw.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


DATABASES = {
    'default_old_cambiareperPostgres': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '',
    },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': config('DB_SQLITE_NAME'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'it-it'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True
USE_THOUSAND_SEPARATOR = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    PROJECT_DIR.parent.child('static'),
)

MEDIA_ROOT = PROJECT_DIR.parent.child('media')
MEDIA_URL = '/uploads/'
WORD_TEMPLATES = MEDIA_ROOT.child('word-templates')

#
# Pannelli da abilitare per Django Debug Toolbar
#
DEBUG_TOOLBAR_PANELS = [
    'ddt_request_history.panels.request_history.RequestHistoryPanel',  # Here it is
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

#
# Aggiunge il supporto di Ajax alla Toolbar
#
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': config('SHOW_TOOLBAR_CALLBACK', cast=lambda v: v if v != '' else lambda r: False),
}

#
# Redirezione dopo il login ed il logout.
#
LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = 'home'

#
# Redirezione per e-mail Backend, così l'e-mail non viene spedita ma solo scritta sulla console. !
#
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Invece adesso le e-mail vengono spedite veramente.
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')

#
# Pagina di Login.
#
LOGIN_URL = 'login'


#
# Settaggi specifici per Django import-export che garantiscono l'incapsulamento delle operazioni.
#
IMPORT_EXPORT_USE_TRANSACTIONS = True

#
# Settaggi per Celery.
#
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_APP_NAME = config('CELERY_APP_NAME')
CELERYSI_DB_QUEUE_NAME = config('CELERYSI_DB_QUEUE_NAME')

#
# Mi dice se non in modalità di test o meno.
#
TESTING = sys.argv[1:2] == ['test']
