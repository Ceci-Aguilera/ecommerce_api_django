import environ
from .base import *

DEBUG = True

env = environ.Env()
# reading env file
environ.Env.read_env()

SECRET_KEY = env("SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': env("DATABASE_HOST"),
        'PORT': env("DATABASE_PORT"),
    }
}


# Email Options for Sending
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
# EMAIL_USE_SSL=True
EMAIL_PORT = 587
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD =  env("EMAIL_HOST_PASSWORD")


# Authentication Options
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = False
