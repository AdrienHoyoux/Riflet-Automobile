from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config.media_views import ServeMediaView

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('api/', include('garage.urls')),
    path('media/<path:path>', ServeMediaView.as_view(), name='serve-media'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'Riflet Automobile — Administration'
admin.site.site_title = 'Riflet Automobile'
admin.site.index_title = 'Gestion du site vitrine'
