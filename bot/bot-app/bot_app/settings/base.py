"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
from distutils.util import strtobool

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# todo: since this is a dev environment key, it is okay to check it into version control
#       although not the best thing to do. in production, the key is overridden.
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d2%c9nrw#-5mifb*$ux4dvjr&2i6u1%f=v9bd!)^ic^zjt38gb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [

]

LOCAL_APPS = [
    # Project apps go here
    'accounts',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bot_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', 'common/templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bot_app.wsgi.application'

# Custom User model
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-user-model
AUTH_USER_MODEL = "accounts.CustomUser"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging settings. Send all the logs to the console.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
            'level': 'INFO',
    },
}

# AWS Settings
AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID", "000000000000")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "FAKEABCDEFGHIJKLMNOP")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "FAKE7NiynG+TogH8Nj+P9nlE73sq3")

# Celery settings
# Check celery good practices: https://denibertovic.com/posts/celery-best-practices/
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "sqs://broker:9324")
# Pass only json serializable arguments to tasks
CELERY_TASK_SERIALIZER = "json"
# We ignore the celery task "result" as we don't need it.
# We keep track of status and/or results in our own DB models as necessary.
CELERY_TASK_IGNORE_RESULT = True
# Queues and routes for celery tasks
CELERY_TASK_DEFAULT_QUEUE = "default"
SQS_DEFAULT_QUEUE_URL = f"http://broker:9324/000000000000/{CELERY_TASK_DEFAULT_QUEUE}"
CELERY_BROKER_TRANSPORT = "sqs"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "region": AWS_REGION_NAME,
    "visibility_timeout": 3600,
    "polling_interval": 5,
    'predefined_queues': {  # We use an SQS queue created previously with CDK
        CELERY_TASK_DEFAULT_QUEUE: {
            'url': SQS_DEFAULT_QUEUE_URL  # Important: Set the queue URL with https:// here when using VPC endpoints
        }
    }
}
# This setting makes the tasks to run synchronously. Useful for local debugging and CI tests.
CELERY_TASK_ALWAYS_EAGER = strtobool(os.getenv("CELERY_TASK_ALWAYS_EAGER", "False"))
