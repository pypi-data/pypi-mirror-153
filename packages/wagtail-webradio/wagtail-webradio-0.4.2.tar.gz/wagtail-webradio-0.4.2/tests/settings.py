import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

VAR_DIR = Path(__file__).parent / 'var'

DEBUG = True if os.environ.get('DEBUG', '0') == '1' else False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'sqlite.db'),
    }
}

SECRET_KEY = 'not needed'

ROOT_URLCONF = 'tests.urls'

STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
]

STATIC_ROOT = VAR_DIR / 'static'

MEDIA_URL = '/media/'

MEDIA_ROOT = VAR_DIR / 'media'

USE_TZ = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INSTALLED_APPS = [
    # django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # wagtail
    'wagtail.sites',
    'wagtail.users',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'taggit',
    # wagtail_webradio
    'wagtail_webradio',
    'tests',
]

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

WAGTAIL_SITE_NAME = 'wagtailradio test'
BASE_URL = 'http://test.local'
