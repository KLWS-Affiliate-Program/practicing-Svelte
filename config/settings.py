"""
Django settings router.
Loads appropriate settings based on ENVIRONMENT variable.
"""

import os

environment = os.getenv("ENVIRONMENT", "development").lower()

if environment == "production":
    from .settings_prod import *
elif environment == "testing":
    from .settings_base import *

    # Test-specific overrides
    DATABASES["default"]["TEST"] = {
        "NAME": "test_" + DATABASES["default"]["NAME"],
    }
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
else:  # Default to development
    from .settings_dev import *
