import mimetypes
import os

from django.conf import settings
from django.http import FileResponse, Http404
from django.views import View


class ServeMediaView(View):
    """Sert les fichiers uploadés (/media/...) en production derrière Traefik."""

    def get(self, request, path):
        media_root = os.path.normpath(str(settings.MEDIA_ROOT))
        full_path = os.path.normpath(os.path.join(media_root, path))

        if not full_path.startswith(media_root):
            raise Http404('Fichier introuvable.')

        if not os.path.isfile(full_path):
            raise Http404('Fichier introuvable.')

        content_type, _ = mimetypes.guess_type(full_path)
        return FileResponse(open(full_path, 'rb'), content_type=content_type or 'application/octet-stream')
