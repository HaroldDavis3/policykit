"""
Django settings for policykit project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    exec(open(BASE_DIR + '/private.py').read())
except IOError:
    print("Unable to open configuration file!")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kg=&9zrc5@rern2=&+6yvh8ip0u7$f=k_zax**bwsur_z7qy+-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['policykit.org',
                 'www.policykit.org',
                 'ec2-52-41-245-161.us-west-2.compute.amazonaws.com',
                 '52.41.245.161',
                 '127.0.0.1',
                 'ec2-54-190-197-117.us-west-2.compute.amazonaws.com',
                 '54.190.197.117']


# Application definition

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'django_celery_results',
    'policyengine',
    'slackintegration',
    'redditintegration',
    'discordintegration'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'policykit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.tz',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'policykit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },

}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


AUTHENTICATION_BACKENDS = ['discordintegration.auth_backends.DiscordBackend',
                           'redditintegration.auth_backends.RedditBackend',
                           'slackintegration.auth_backends.SlackBackend',
                           'django.contrib.auth.backends.ModelBackend']


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

PROJECT_NAME = "PolicyKit"


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'slackintegration': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'redditintegration': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'discordintegration': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'policyengine': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


from celery.schedules import crontab

CELERY_BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'


CELERY_BEAT_SCHEDULE = {
 'count-votes-beat': {
       'task': 'policyengine.tasks.consider_proposed_actions',
       'schedule': 60.0,
    },
 'reddit-listener-beat': {
       'task': 'redditintegration.tasks.reddit_listener_actions',
       'schedule': 60.0,
    },
 'discord-listener-beat': {
       'task': 'discordintegration.tasks.discord_listener_actions',
       'schedule': 60.0,
    }
}


JET_DEFAULT_THEME = 'default'


JET_INDEX_DASHBOARD = 'policykit.dashboard.CustomIndexDashboard'
JET_APP_INDEX_DASHBOARD = 'policykit.dashboard.CustomAppIndexDashboard'
