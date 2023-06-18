# Python
import decouple
from pathlib import Path
import sys
import os
import mimetypes
import datetime

# Sentry
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'backend'))

SECRET_KEY = decouple.config('SECRET_KEY', cast=str)

DEBUG = decouple.config('DEBUG', cast=bool)

ALLOWED_HOSTS = (
    '127.0.0.1',
)

AUTH_USER_MODEL = 'auths.User'

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',

    'debug_toolbar',
    'django_extensions',
    'rest_framework',
    'rest_framework_simplejwt',
)

CUSTOM_APPS = (
    'abstracts',
    'auths',
    'bank',

    'frontend',
)

INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS

AUTHENTICATION_BACKENDS = (
    'auths.backends.UserBackend',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

ROOT_URLCONF = 'settings.urls'

TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ('templates',),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ),
        },
    },
)

WSGI_APPLICATION = 'settings.wsgi.application'

DB_NAME = decouple.config('DB_NAME', cast=str)
DB_USER = decouple.config('DB_USER', cast=str)
DB_PASS = decouple.config('DB_PASS', cast=str)
DB_HOST = decouple.config('DB_HOST', cast=str)
DB_PORT = decouple.config('DB_PORT', cast=str)

if DEBUG is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'testdb.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASS,
            'HOST': DB_HOST,
            'PORT': DB_PORT
        }
    }

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

APPEND_SLASH = False

ALLOWED_DOMAINS: tuple[str, ...] = ('inbox.ru', 'mail.ru',
                                    'list.ru', 'gmail.com')

# CELERY
# ---------------------------------------------------------------------

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

# CURRENCY
# ---------------------------------------------------------------------

ALLOWED_CURRENCY = (
    'KZT',
    'RUB',
    'EUR',
    'USD'
)

EXCHANGE_RATES_URL = decouple.config('EXCHANGE_RATES_URL', cast=str)

# ENCRYPT
# ---------------------------------------------------------------------

FERNET_KEY = decouple.config('FERNET_KEY', cast=str)
FERNET_KEY = bytes(FERNET_KEY, encoding='utf-8')

# EMAIL-HOST
# ---------------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = decouple.config('EMAIL_HOST', cast=str)
EMAIL_HOST_USER = decouple.config('EMAIL_HOST_USER', cast=str)
EMAIL_HOST_PASSWORD = decouple.config('EMAIL_HOST_PASSWORD', cast=str)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# CORS-HEADERS
# ---------------------------------------------------------------------

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = (
    'http://127.0.0.1',
)

CORS_URLS_REGEX = r'^/api/.*$'


# DEBUG-TOOLBAR
# ---------------------------------------------------------------------

mimetypes.add_type('application/javascript', '.js', True)

INTERNAL_IPS = (
    '127.0.0.1',
)

# SENTRY-SDK
# ---------------------------------------------------------------------

sentry_sdk.init(
    dsn=decouple.config('SENTRY_SDK_DSN', cast=str),
    integrations=(
        DjangoIntegration(),
    ),
    traces_sample_rate=1.0
)

# DRF
# ---------------------------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# SIMPLE JWT
# ---------------------------------------------------------------------

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(hours=3),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.AccessToken',
    ),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainPairSerializer',
    'TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSerializer',
    'TOKEN_VERIFY_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenVerifySerializer',
    'TOKEN_BLACKLIST_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenBlacklistSerializer',

    'SLIDING_TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer',
    'SLIDING_TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer',
}
