from .base import *

DEBUG = env("DEBUG")

DJANGO_APPS += []

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(" ")

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'djoser',
    'django_filters',
]

LOCAL_APPS = [
    "apps.users",
    "apps.bankcontroller"
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
