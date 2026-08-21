import os
from django.core.asgi import get_asgi_application

# Cambiamos la configuración para que apunte al nuevo nombre de retail
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventarioretail.settings')

application = get_asgi_application()
