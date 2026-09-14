"""Django settings for the BLIP project."""

from pathlib import Path
import os
import sys
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

if (BASE_DIR / '.env').exists():
    load_dotenv(BASE_DIR / '.env')


def _get_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


def _get_csv(name: str, default=None):
    value = os.environ.get(name, '')
    items = [item.strip() for item in value.split(',') if item.strip()]
    if items:
        return items
    return default or []


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured('DJANGO_SECRET_KEY must be set.')

DEBUG = _get_bool('DJANGO_DEBUG', False)

render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
ALLOWED_HOSTS = _get_csv('DJANGO_ALLOWED_HOSTS', ['localhost', '127.0.0.1'] if DEBUG else [])
if render_host:
    ALLOWED_HOSTS.append(render_host)
if not DEBUG and not ALLOWED_HOSTS:
    raise ImproperlyConfigured('DJANGO_ALLOWED_HOSTS must be set in production.')

if not DEBUG and len(SECRET_KEY) < 50:
    raise ImproperlyConfigured('DJANGO_SECRET_KEY must be at least 50 characters in production.')

CSRF_TRUSTED_ORIGINS = _get_csv('DJANGO_CSRF_TRUSTED_ORIGINS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'posts',
    'tailwind',
    'theme',
]

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ['127.0.0.1']
NPM_BIN_PATH = os.environ.get('NPM_BIN_PATH', r'C:\Program Files\nodejs\npm.cmd')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blip.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blip.wsgi.application'

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    parsed = urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parsed.path.lstrip('/') or os.environ.get('POSTGRES_DB', 'postgres'),
            'USER': parsed.username or os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': parsed.password or os.environ.get('POSTGRES_PASSWORD', ''),
            'HOST': parsed.hostname or os.environ.get('POSTGRES_HOST', 'localhost'),
            'PORT': str(parsed.port or os.environ.get('POSTGRES_PORT', '5432')),
        }
    }
else:
    postgres_host = os.environ.get('POSTGRES_HOST')
    if postgres_host:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('POSTGRES_DB', 'blip'),
                'USER': os.environ.get('POSTGRES_USER', 'blip'),
                'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
                'HOST': postgres_host,
                'PORT': os.environ.get('POSTGRES_PORT', '5432'),
            }
        }
    else:
        DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/posts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'same-origin'

TESTING = 'test' in sys.argv

if not DEBUG and not TESTING:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
