import logging
import os

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def notify_contact_message(contact) -> bool:
    """Envoie une notification e-mail lors d'un nouveau message de contact."""
    recipient = getattr(settings, 'CONTACT_NOTIFICATION_EMAIL', '') or os.getenv(
        'CONTACT_EMAIL', ''
    )
    if not recipient:
        logger.warning('CONTACT_EMAIL non configuré — notification ignorée.')
        return False

    if not settings.EMAIL_HOST:
        logger.warning(
            'EMAIL_HOST non configuré — message #%s enregistré sans envoi e-mail.',
            contact.pk,
        )
        return False

    subject = f'[Riflet Automobile] {contact.subject}'
    body = (
        f'Nouveau message via le formulaire de contact\n\n'
        f'Nom : {contact.name}\n'
        f'E-mail : {contact.email}\n'
        f'Téléphone : {contact.phone or "—"}\n'
        f'Sujet : {contact.subject}\n\n'
        f'Message :\n{contact.message}\n'
    )

    try:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            reply_to=[contact.email],
        )
        email.send(fail_silently=False)
        logger.info('Notification contact #%s envoyée à %s', contact.pk, recipient)
        return True
    except Exception:
        logger.exception(
            'Échec envoi e-mail pour le message de contact #%s', contact.pk
        )
        return False
