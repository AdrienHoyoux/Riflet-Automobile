import html
import json
import logging
import os
import socket
import urllib.error
import urllib.request

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.formats import date_format
from django.utils.timezone import localtime

logger = logging.getLogger(__name__)

SITE_URL = os.getenv('NUXT_PUBLIC_SITE_URL', 'https://hoyouxcorp.com').rstrip('/')


def _format_received_at(contact) -> str:
    created = getattr(contact, 'created_at', None)
    if not created:
        return date_format(localtime(), 'DATETIME_FORMAT')
    return date_format(localtime(created), 'DATETIME_FORMAT')


def _contact_email_content(contact) -> tuple[str, str, str]:
    subject = f'[Riflet Automobile] {contact.subject}'
    phone = contact.phone or '—'
    received_at = _format_received_at(contact)

    text_body = (
        f'Nouveau message via le formulaire de contact\n'
        f'{"=" * 40}\n\n'
        f'Nom       : {contact.name}\n'
        f'E-mail    : {contact.email}\n'
        f'Téléphone : {phone}\n'
        f'Sujet     : {contact.subject}\n'
        f'Reçu le   : {received_at}\n\n'
        f'Message :\n'
        f'{"-" * 40}\n'
        f'{contact.message}\n'
        f'{"-" * 40}\n\n'
        f'Répondre à : {contact.email}\n'
    )

    html_body = _contact_email_html(contact, phone, received_at)
    return subject, text_body, html_body


def _contact_email_html(contact, phone: str, received_at: str) -> str:
    name = html.escape(contact.name)
    email = html.escape(contact.email)
    phone_display = html.escape(phone)
    subject = html.escape(contact.subject)
    message = html.escape(contact.message).replace('\n', '<br>')
    site_url = html.escape(SITE_URL)
    mailto = html.escape(f'mailto:{contact.email}')

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nouveau message — Riflet Automobile</title>
</head>
<body style="margin:0;padding:0;background-color:#f5f2ea;font-family:Arial,Helvetica,sans-serif;color:#0a0a0a;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color:#f5f2ea;padding:32px 16px;">
    <tr>
      <td align="center">
        <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="max-width:600px;width:100%;">

          <!-- En-tête -->
          <tr>
            <td style="background-color:#0a0a0a;padding:28px 32px;border:2px solid #0a0a0a;">
              <p style="margin:0 0 6px;font-size:11px;font-weight:bold;letter-spacing:0.12em;text-transform:uppercase;color:#d4ff00;">
                Formulaire de contact
              </p>
              <h1 style="margin:0;font-size:28px;font-weight:bold;letter-spacing:0.06em;text-transform:uppercase;color:#f5f2ea;line-height:1.2;">
                Riflet Automobile
              </h1>
            </td>
          </tr>
          <tr>
            <td style="height:4px;background-color:#d4ff00;font-size:0;line-height:0;">&nbsp;</td>
          </tr>

          <!-- Sujet -->
          <tr>
            <td style="background-color:#ffffff;padding:24px 32px;border-left:2px solid #0a0a0a;border-right:2px solid #0a0a0a;">
              <p style="margin:0 0 4px;font-size:11px;font-weight:bold;letter-spacing:0.1em;text-transform:uppercase;color:#8a8a8a;">
                Sujet
              </p>
              <p style="margin:0;font-size:20px;font-weight:bold;color:#0a0a0a;line-height:1.3;">
                {subject}
              </p>
              <p style="margin:8px 0 0;font-size:12px;color:#8a8a8a;">
                Reçu le {html.escape(received_at)}
              </p>
            </td>
          </tr>

          <!-- Coordonnées -->
          <tr>
            <td style="background-color:#ffffff;padding:8px 32px 24px;border-left:2px solid #0a0a0a;border-right:2px solid #0a0a0a;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse;">
                <tr>
                  <td style="padding:12px 0;border-bottom:1px solid #e8e4da;width:120px;vertical-align:top;">
                    <span style="font-size:11px;font-weight:bold;letter-spacing:0.08em;text-transform:uppercase;color:#8a8a8a;">Nom</span>
                  </td>
                  <td style="padding:12px 0;border-bottom:1px solid #e8e4da;font-size:15px;color:#0a0a0a;">
                    {name}
                  </td>
                </tr>
                <tr>
                  <td style="padding:12px 0;border-bottom:1px solid #e8e4da;vertical-align:top;">
                    <span style="font-size:11px;font-weight:bold;letter-spacing:0.08em;text-transform:uppercase;color:#8a8a8a;">E-mail</span>
                  </td>
                  <td style="padding:12px 0;border-bottom:1px solid #e8e4da;font-size:15px;">
                    <a href="{mailto}" style="color:#0a0a0a;text-decoration:underline;">{email}</a>
                  </td>
                </tr>
                <tr>
                  <td style="padding:12px 0;vertical-align:top;">
                    <span style="font-size:11px;font-weight:bold;letter-spacing:0.08em;text-transform:uppercase;color:#8a8a8a;">Téléphone</span>
                  </td>
                  <td style="padding:12px 0;font-size:15px;color:#0a0a0a;">
                    {phone_display}
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Message -->
          <tr>
            <td style="background-color:#ffffff;padding:0 32px 28px;border-left:2px solid #0a0a0a;border-right:2px solid #0a0a0a;">
              <p style="margin:0 0 10px;font-size:11px;font-weight:bold;letter-spacing:0.1em;text-transform:uppercase;color:#8a8a8a;">
                Message
              </p>
              <div style="background-color:#f5f2ea;border:2px solid #0a0a0a;padding:20px;font-size:15px;line-height:1.6;color:#0a0a0a;">
                {message}
              </div>
            </td>
          </tr>

          <!-- Actions -->
          <tr>
            <td style="background-color:#ffffff;padding:0 32px 32px;border-left:2px solid #0a0a0a;border-right:2px solid #0a0a0a;border-bottom:2px solid #0a0a0a;">
              <a href="{mailto}" style="display:inline-block;background-color:#d4ff00;color:#0a0a0a;font-size:12px;font-weight:bold;letter-spacing:0.1em;text-transform:uppercase;text-decoration:none;padding:14px 24px;border:2px solid #0a0a0a;">
                Répondre
              </a>
            </td>
          </tr>

          <!-- Pied de page -->
          <tr>
            <td style="padding:20px 8px 0;text-align:center;">
              <p style="margin:0;font-size:12px;color:#8a8a8a;line-height:1.5;">
                <a href="{site_url}" style="color:#8a8a8a;text-decoration:underline;">{site_url}</a><br>
                Avenue de Norvège 3, 4960 Malmedy — 080 39 99 81
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def _send_via_resend(
    subject: str,
    text_body: str,
    recipient: str,
    reply_to: str,
    html_body: str | None = None,
) -> bool:
    api_key = os.getenv('RESEND_API_KEY', '').strip()
    if not api_key:
        return False

    from_email = os.getenv(
        'RESEND_FROM_EMAIL',
        settings.DEFAULT_FROM_EMAIL or 'Riflet Automobile <noreply@hoyouxcorp.com>',
    )
    payload: dict = {
        'from': from_email,
        'to': [recipient],
        'reply_to': reply_to,
        'subject': subject,
        'text': text_body,
    }
    if html_body:
        payload['html'] = html_body

    request = urllib.request.Request(
        'https://api.resend.com/emails',
        data=json.dumps(payload).encode('utf-8'),
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


def _send_via_smtp(
    subject: str,
    text_body: str,
    recipient: str,
    reply_to: str,
    html_body: str | None = None,
) -> bool:
    if not settings.EMAIL_HOST:
        return False

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
        reply_to=[reply_to],
    )
    if html_body:
        email.attach_alternative(html_body, 'text/html')
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

    subject, text_body, html_body = _contact_email_content(contact)
    reply_to = contact.email

    if os.getenv('RESEND_API_KEY', '').strip():
        if _send_via_resend(subject, text_body, recipient, reply_to, html_body):
            return True
        logger.warning('Resend indisponible — tentative SMTP pour le message #%s', contact.pk)

    try:
        return _send_via_smtp(subject, text_body, recipient, reply_to, html_body)
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
