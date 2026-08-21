# Busca esta línea (aproximadamente en la línea 70) y cámbiala a:
ROOT_URLCONF = 'inventarioretail.urls'

# Busca esta línea (aproximadamente en la línea 110) y cámbiala a:
WSGI_APPLICATION = 'inventarioretail.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tu aplicación de gestión de inventario retail vinculada
    'articulos',
]
