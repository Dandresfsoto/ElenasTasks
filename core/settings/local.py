import sys

from core.settings.base import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-sdb^6%tk#6wpdgsn_1q6#k=@mn*u)j_3gvp=@#oqycm1_(z5m*')

ALLOWED_HOSTS = ["*"]

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB_TEST'),
        'USER': os.environ.get('POSTGRES_USER_TEST'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD_TEST'),
        'HOST': os.environ.get('POSTGRES_HOST_TEST'),
        'PORT': os.environ.get('POSTGRES_PORT_TEST')
    }
