"""
ASGI config for Project Horizon.
Supports WebSockets via Daphne.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Fallback to standard ASGI for now - add websocket support as needed
application = get_asgi_application()
