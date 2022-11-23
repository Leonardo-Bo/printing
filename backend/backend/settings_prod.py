"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import json

with open('/etc/config.json') as config_file:
    config = json.load(config_file)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['printing.bio-groups.com']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # )
}

DOMAIN = 'printing.bio-groups.com'
SITE_NAME = 'printing.bio-groups'
TEAM = 'bio-groups'

DJOSER = {
    "USER_CREATE_PASSWORD_RETYPE": True, 
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True, 
    "PASSWORD_RESET_CONFIRM_URL": "reset-password/confirm/{uid}/{token}",
    
    "SERIALIZERS": {
        "user_create": "apps.accounts.serializers.UserCreateSerializer",
        "user": "apps.accounts.serializers.UserSerializer",
        "current_user": "apps.accounts.serializers.UserSerializer",
        "user_delete": "djoser.serializers.UserDeleteSerializer"
    }
}

AUTH_USER_MODEL = 'accounts.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',

    'apps.crossuser',
    'apps.accounts',
    'apps.research',
    'apps.publications',
    'apps.news',
    'apps.people',
    'apps.carousel',
    'apps.tools',

    'apps.images',
    'apps.files'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.joinpath('templates')
        ],
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

WSGI_APPLICATION = 'backend.wsgi.application'


USERS_DB = 'users'

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'printing',
       'USER': config.get('DB_USER'),
       'PASSWORD': config.get('DB_PASS'),
       'HOST': 'postgres-biogroup',
       'PORT':'',
   },
   USERS_DB: {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'printing_users',
       'USER': config.get('DB_USER'),
       'PASSWORD': config.get('DB_PASS'),
       'HOST': 'postgres-biogroup',
       'PORT':'',
   },
}

DATABASE_ROUTERS = ['backend.routers.AuthRouter']


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
# STATICFILES_DIRS = [
#     BASE_DIR.joinpath('static')
# ]
STATIC_ROOT = BASE_DIR.joinpath('static')

MEDIA_ROOT = BASE_DIR.joinpath("media")
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config.get('EMAIL_SYSTEM')
EMAIL_HOST_PASSWORD = config.get('EMAIL_PASS')

ADMINS = ((os.environ.get('USER_ADMIN'), os.environ.get('EMAIL_ADMIN')), )