import re

MEDIA_PATH_RE = re.compile(r'/media/[^\s?#]+')


def normalize_media_path(url):
    """Chemin relatif /media/... ou URL externe https:// ; jamais d'hôte Docker interne."""
    if not url:
        return None

    value = str(url).strip()
    if not value:
        return None

    if value.startswith('/media/'):
        return value

    match = MEDIA_PATH_RE.search(value)
    if match:
        return match.group(0)

    if value.startswith(('http://', 'https://')):
        return value

    return value if value.startswith('/') else f'/{value}'


def public_media_url(url):
    """URL publique pour les réponses API (HTTPS en prod)."""
    path = normalize_media_path(url)
    if not path:
        return None
    if path.startswith('/media/'):
        from django.conf import settings

        return f'{settings.PUBLIC_SITE_URL}{path}'
    return path
