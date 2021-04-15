import os

from core.settings.base import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Todo: update this list
ALLOWED_HOSTS = ["dandresfsoto.com", "www.dandresfsoto.com"]
