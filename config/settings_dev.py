"""
Django settings for local development.
Extends base settings with dev-specific overrides.
"""

from .settings_base import *

DEBUG = True
ALLOWED_HOSTS += ["*"]

# Database - keep default (PostgreSQL in Docker)
# DATABASES already defined in base

# Add debug toolbar
INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ["127.0.0.1"]

# Development email backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Disable security checks for local development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# More verbose logging in development
LOGGING["loggers"]["django"]["level"] = "DEBUG"
LOGGING["loggers"]["apps"]["level"] = "DEBUG"

# Disable whitenoise manifest for faster dev reloads
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Simple cache for dev (in-memory)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
