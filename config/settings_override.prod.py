import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'production').lower()
ALLOWED_HOSTS = [
    '.{0}'.format(os.environ['WEB_DOMAIN']),
]
# Used For wildcard domain accessing
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True # this should be handled by DNS or nginx-proxy
# SECURE_HSTS_SECONDS = 31536000 # Again, its already added by nginx-proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://{2}:{0}@{1}:6379/1'.format(
            os.environ['REDIS_PASSWORD'],
            os.environ['REDIS_SERVICE'],
            os.environ.get('REDIS_USER', '')
        ),
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['PGB_SERVICE'],
        'PORT': os.environ['PGB_PORT'],
    },
}
STATIC_ROOT = '/app/static/'
MEDIA_ROOT = '/app/media/'
# Defualt
# MEDIA_URL = 'https://{0}/media/'.format(os.environ['WEB_DOMAIN'])
# STATIC_URL = 'https://{0}/static/'.format(os.environ['WEB_DOMAIN'])
# CDN/S3
# MEDIA_URL = 'https://media.{0}/'.format(os.environ['WEB_DOMAIN'])
# STATIC_URL = 'https://media.{0}/assets/'.format(os.environ['WEB_DOMAIN'])