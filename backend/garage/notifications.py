import json
import logging
import os
import socket
import urllib.error
import urllib.request

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def _contact_email_content(contact) -> tuple[str, str]:
    subject = f'[Riflet Automobile] {contact.subject}'
    body = (
        f'Nouveau message via le formulaire de contact\n\n'
        f'Nom : {contact.name}\n'
        f'E-mail : {contact.email}\n'
        f'Téléphone : {contact.phone or "—"}\n'
        f'Sujet : {contact.subject}\n\n'
        f'Message :\n{contact.message}\n'
    )
    return subject, body


def _send_via_resend(
    subject: str,
    body: str,
    recipient: str,
    reply_to: str,
) -> bool:
    api_key = os.getenv('RESEND_API_KEY', '').strip()
    if not api_key:
        return False

    from_email = os.getenv(
        'RESEND_FROM_EMAIL',
        settings.DEFAULT_FROM_EMAIL or 'Riflet Automobile <noreply@hoyouxcorp.com>',
    )
    payload = json.dumps({
        'from': from_email,
        'to': [recipient],
        'reply_to': reply_to,
        'subject': subject,
        'text': body,
    }).encode('utf-8')

    request = urllib.request.Request(
        'https://api.resend.com/emails',
        data=payload,
        method='POST',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response.read()
        logger.info('Notification Resend envoyée à %s', recipient)
        return True
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode('utf-8', errors='replace')
        logger.error('Resend HTTP %s : %s', exc.code, detail)
        return False
    except Exception:
        logger.exception('Échec envoi Resend')
        return False


def _send_via_smtp(subject: str, body: str, recipient: str, reply_to: str) -> bool:
    if not settings.EMAIL_HOST:
        return False

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
        reply_to=[reply_to],
    )
    email.send(fail_silently=False)
    logger.info('Notification SMTP envoyée à %s', recipient)
    return True


def notify_contact_message(contact) -> bool:
    """Envoie une notification e-mail lors d'un nouveau message de contact."""
    recipient = getattr(settings, 'CONTACT_NOTIFICATION_EMAIL', '') or os.getenv(
        'CONTACT_EMAIL', ''
    )
    if not recipient:
        logger.warning('CONTACT_EMAIL non configuré — notification ignorée.')
        return False

    subject, body = _contact_email_content(contact)
    reply_to = contact.email

    if os.getenv('RESEND_API_KEY', '').strip():
        if _send_via_resend(subject, body, recipient, reply_to):
            return True
        logger.warning('Resend indisponible — tentative SMTP pour le message #%s', contact.pk)

    try:
        return _send_via_smtp(subject, body, recipient, reply_to)
    except Exception:
        logger.exception(
            'Échec envoi e-mail pour le message de contact #%s', contact.pk
        )
        return False


def check_smtp_connectivity() -> tuple[bool, str]:
    """Teste la connexion TCP vers le serveur SMTP configuré."""
    host = settings.EMAIL_HOST
    port = settings.EMAIL_PORT
    if not host:
        return False, 'EMAIL_HOST non configuré'

    try:
        with socket.create_connection((host, port), timeout=10):
            pass
        return True, f'Connexion OK vers {host}:{port}'
    except OSError as exc:
        return False, f'Connexion refusée vers {host}:{port} — {exc}'
