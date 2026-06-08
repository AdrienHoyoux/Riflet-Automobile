from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('api/', include('garage.urls')),
]

# Fichiers uploadés (admin) — servis par Django derrière Traefik / nginx en prod
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'Riflet Automobile — Administration'
admin.site.site_title = 'Riflet Automobile'
admin.site.index_title = 'Gestion du site vitrine'
