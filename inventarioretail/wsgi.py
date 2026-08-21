import os
from django.core.wsgi import get_wsgi_application

# Cambiamos la configuración para que apunte al nuevo nombre de retail
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventarioretail.settings')

application = get_wsgi_application()
