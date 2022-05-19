import os
from .settings_default import *

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.getenv('DEBUG', 'NO').lower() in ('on', 'true', 'y', 'yes')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'staging').lower()
ALLOWED_HOSTS = [
    '127.0.0.1', 'localhost',
    '0.0.0.0',  # running in docker
    '.{0}'.format(os.environ['WEB_DOMAIN']),
]

CSRF_TRUSTED_ORIGINS = ['https://*.{0}'.format(os.environ['WEB_DOMAIN']),]
STATIC_URL = 'static/'
MEDIA_URL = 'media/'
# Application Settings ###

REQUIRED_APPS = [
    # RESTful
    'rest_framework',
    'oauth2_provider',
    'corsheaders',
    # Other
    'auth_framework',
]
LOCAL_APPS = [
    'auth.apps.AuthConfig',
]
INSTALLED_APPS += REQUIRED_APPS
INSTALLED_APPS += LOCAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Authentication Settings ###
AUTH_USER_MODEL = 'custom_auth.User'
AUTH_PASSWORD_VALIDATORS = [  # Reset Auth Password Validators for customization
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
]

AUTH_FRAMEWORK = {
    'WITH_PHONENUMBER_FIELD': False,
    'USE_PASSWORD_TWICE_VALIDATION': False,
    'SERIALIZERS': {
        'SIGNUP_SERIALIZER': 'auth.serializers.ExtendSignUpSerializer',
        'USERINFO_SERIALIZER': 'auth.serializers.ExtendUserInfoSerializer'
    },
}

AUTHENTICATION_BACKENDS = [
    "auth_framework.backends.auth_backends.AuthenticationBackend",
]

OAUTH2_PROVIDER = {
    "OIDC_ENABLED": True,
    "OIDC_RSA_PRIVATE_KEY": os.environ.get('OIDC_RSA_PRIVATE_KEY'),
    'SCOPES': {
        "openid": "OpenID Connect scope",
        'read': 'Read scope',
        'write': 'Write scope',
    },
    'OAUTH2_VALIDATOR_CLASS': 'auth_framework.oauth.oauth2_validators.OauthValidator',
    'OAUTH2_BACKEND_CLASS': 'auth_framework.oauth.oauth2_backends.OAuthLibCore',
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600 * 24 * 30,
    'REFRESH_TOKEN_EXPIRE_SECONDS': 3600 * 24 * 30 * 2,
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
PHONENUMBER_DEFAULT_REGION = 'US'
# Restful Settings ###
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'EXCEPTION_HANDLER': 'general.utils.custom_exception_handler'
}
CORS_ORIGIN_REGEX_WHITELIST = (
    r'^(https?://)?(\w+\.)*?{0}$'.format(os.environ['WEB_DOMAIN']),
    r'^http://localhost:(8000|3000)$',
    r'^http://127.0.0.1:(8000|3000)$',
)
CORS_ALLOW_CREDENTIALS = True

# Email Settings ###
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', )
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# Other Frameworks Settings ###
# Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": ["redis://:{0}@{1}:6379/0".format(os.environ['REDIS_PASSWORD'],
                                                       os.environ['REDIS_SERVICE'])],
        },
    },
}
# Sentry
if os.environ.get('SENTRY_DSN'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        integrations=[DjangoIntegration()],
        send_default_pii=True,
        environment=ENVIRONMENT
    )
if os.environ.get('SOLR_SERVICE'):
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'general.backends.solr_backends.SolrEngine',  # 'haystack.backends.solr_backend.SolrEngine'
            'URL': 'http://{}:8983/solr/default'.format(os.environ['SOLR_SERVICE'])
        },
    }
# Celery
if os.environ.get('SOLR_SERVICE'):
    CELERY_BROKER_URL = 'redis://:{0}{1}:6379/0'.format(os.environ['REDIS_PASSWORD'],
                                                         os.environ['REDIS_SERVICE'])
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL

try:
    LOCAL_INSTALLED_APPS = []
    from .settings_override import *
    import re
    INSTALLED_APPS += LOCAL_INSTALLED_APPS
    if DEBUG:
        INSTALLED_APPS += ['debug_toolbar', ]
        MIDDLEWARE = [
            'general.middleware.SqlPrintingMiddleware',
            'debug_toolbar.middleware.DebugToolbarMiddleware',
                     ] + MIDDLEWARE
        # DRF post wont trigger window.djdt.init() to display django debugger btn.
        # runserver in Docker docker would give container REMOTE_ADDR to request
        # To fix this, a custom SHOW_TOOLBAR_CALLBACK or let REMOTE_ADDR in INTERNAL_IPS always return True:
        # INTERNAL_IPS = type(str('c'), (), {'__contains__': lambda *a: True})()
        DEBUG_TOOLBAR_CONFIG = {
            "SHOW_TOOLBAR_CALLBACK":
                lambda request: 'admin' not in request.path and
                                re.search(r'Chrome|Mozilla|Safari', request.headers.get('User-Agent', '')),
        }

except ImportError:
    pass
