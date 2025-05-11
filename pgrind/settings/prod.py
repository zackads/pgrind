from .base import *

import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Google Cloud Run terminates HTTPS at the load balancer, so same-domain requests
# look like cross-origin requests to Django.  This must be set to the deployed
# URL.
DJANGO_CSRF_TRUSTED_ORIGINS = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(
    ","
)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")

# Redirect all HTTP traffic to HTTPS
SECURE_SSL_REDIRECT = True
