"""
ASGI config for subeteyabackend project.

Exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from django.core.asgi import get_asgi_application
import socketio
from socketio_app.sio import sio  # importamos el servidor Socket.IO

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "subeteyabackend.settings")

# ASGI de Django para HTTP normal
django_asgi_app = get_asgi_application()

# Aplicación ASGI combinada:
# - HTTP -> django_asgi_app
# - Socket.IO/WebSocket -> manejado por `sio`
application = socketio.ASGIApp(sio, django_asgi_app)
