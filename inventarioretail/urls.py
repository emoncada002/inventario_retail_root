from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from articulos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard_retail, name='dashboard'),
]

# Esto le prermite a Django servir archivos de medios (imágenes, videos, etc.)
# durante el desarrollo.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
