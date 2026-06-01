from django.conf import settings
from django.core.management.base import BaseCommand

from garage.models import ContactMessage
from garage.notifications import (
    _contact_email_content,
    _send_via_smtp,
    check_smtp_connectivity,
)


class Command(BaseCommand):
    help = 'Teste la configuration SMTP du formulaire de contact.'

    def handle(self, *args, **options):
        recipient = settings.CONTACT_NOTIFICATION_EMAIL or settings.DEFAULT_FROM_EMAIL
        if not recipient:
            self.stderr.write(self.style.ERROR('CONTACT_EMAIL non configuré.'))
            return

        self.stdout.write(f'Boîte de réception (CONTACT_EMAIL) : {recipient}')
        self.stdout.write(f'Expéditeur SMTP (DEFAULT_FROM_EMAIL) : {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'EMAIL_HOST={settings.EMAIL_HOST or "(vide)"}')
        self.stdout.write(f'EMAIL_PORT={settings.EMAIL_PORT}')
        self.stdout.write(f'EMAIL_USE_TLS={settings.EMAIL_USE_TLS}')
        self.stdout.write(f'EMAIL_USE_SSL={settings.EMAIL_USE_SSL}')

        if not settings.EMAIL_HOST:
            self.stderr.write(self.style.ERROR('EMAIL_HOST non configuré.'))
            return

        ok, message = check_smtp_connectivity()
        if ok:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stderr.write(self.style.ERROR(message))
            return

        sample = ContactMessage(
            name='Jean Dupont',
            email='client@example.com',
            phone='0470 12 34 56',
            subject='Demande de rendez-vous',
            message='Bonjour,\n\nJe souhaiterais prendre rendez-vous pour un entretien.\n\nMerci.',
        )
        subject, text_body, html_body = _contact_email_content(sample)

        self.stdout.write('Envoi test via SMTP...')
        try:
            if _send_via_smtp(subject, text_body, recipient, sample.email, html_body):
                self.stdout.write(self.style.SUCCESS(f'SMTP : envoyé à {recipient}'))
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f'SMTP : échec — {exc}'))
