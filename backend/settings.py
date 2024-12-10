"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from typing import Any

import django_stubs_ext

django_stubs_ext.monkeypatch()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

ENV = os.getenv('ENV', 'dev')

IS_PROD = ENV == 'prod'
IS_TEST = ENV == 'test'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not IS_PROD

APPEND_SLASH = True

ALLOWED_HOSTS: list[str] = [
    'localhost',
    '127.0.0.1',
    '192.168.1.85',
    'v2134454.hosted-by-vdsina.ru',
    'solidsign.ru',
]

CSRF_TRUSTED_ORIGINS: list[str] = [
    'http://localhost',
    'http://127.0.0.1',
    'https://v2134454.hosted-by-vdsina.ru',
    'https://solidsign.ru',
]

CORS_ALLOWED_ORIGINS: list[str] = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://solidsign.ru',
]

INTERNAL_IPS: list[str] = [
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'tailwind',
    'meta',
    *(['django_browser_reload'] if DEBUG else []),
    'theme',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    *(['django_browser_reload.middleware.BrowserReloadMiddleware'] if DEBUG else []),
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
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.menu',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DEFAULT_DB = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db' / 'db.sqlite3',
}

if IS_TEST:
    DEFAULT_DB = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }


DATABASES = {'default': DEFAULT_DB}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'https://cdn.solisign.ru/'
# STATIC_URL = 'https://storage.yandexcloud.net/solidsign/'
if not IS_PROD:
    STATIC_URL = 'static/'
    MEDIA_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TAILWIND_APP_NAME = 'theme'

YANDEX_OBJECT_STORAGE: dict[str, Any] = {
    'BACKEND': 'storages.backends.s3.S3Storage',
    'OPTIONS': {
        'bucket_name': 'solidsign',
        'access_key': os.getenv('S3_CLIENT_ID'),
        'secret_key': os.getenv('S3_CLIENT_SECRET'),
        'endpoint_url': 'https://storage.yandexcloud.net',
        'querystring_auth': False,
    },
}
STATIC_STORAGE = DEFAULT_STORAGE = YANDEX_OBJECT_STORAGE


if IS_PROD:
    STORAGES = {
        'default': DEFAULT_STORAGE,
        'staticfiles': STATIC_STORAGE,
    }


META_USE_OG_PROPERTIES = True
META_DEFAULT_KEYWORDS = ['solid', 'sign', 'solidsign', 'techno', 'hard techno', 'schranz', 'Набережные Челны', 'техно']
META_SITE_NAME = 'SOLID SIGN'
META_SITE_PROTOCOL = 'https'
