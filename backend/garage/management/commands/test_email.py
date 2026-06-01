from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from garage.notifications import _send_via_resend, check_smtp_connectivity


class Command(BaseCommand):
    help = 'Teste la configuration e-mail (SMTP et/ou Resend).'

    def handle(self, *args, **options):
        recipient = settings.CONTACT_NOTIFICATION_EMAIL or settings.DEFAULT_FROM_EMAIL
        if not recipient:
            self.stderr.write(self.style.ERROR('CONTACT_EMAIL non configuré.'))
            return

        self.stdout.write(f'Destinataire test : {recipient}')
        self.stdout.write(f'EMAIL_HOST={settings.EMAIL_HOST or "(vide)"}')
        self.stdout.write(f'EMAIL_PORT={settings.EMAIL_PORT}')
        self.stdout.write(f'EMAIL_USE_TLS={settings.EMAIL_USE_TLS}')
        self.stdout.write(f'EMAIL_USE_SSL={settings.EMAIL_USE_SSL}')
        self.stdout.write(f'RESEND_API_KEY={"oui" if settings.RESEND_API_KEY else "non"}')

        if settings.EMAIL_HOST:
            ok, message = check_smtp_connectivity()
            if ok:
                self.stdout.write(self.style.SUCCESS(message))
            else:
                self.stdout.write(self.style.ERROR(message))
                self.stdout.write(
                    'Les VPS Hostinger bloquent souvent le port 587. '
                    'Essayez le port 465 (EMAIL_USE_SSL=True) ou Resend (RESEND_API_KEY).'
                )

        if settings.RESEND_API_KEY:
            self.stdout.write('Envoi test via Resend...')
            if _send_via_resend(
                'Test Riflet Automobile',
                'E-mail de test depuis le serveur de production.',
                recipient,
                recipient,
            ):
                self.stdout.write(self.style.SUCCESS('Resend : envoyé'))
                return
            self.stdout.write(self.style.ERROR('Resend : échec'))

        if settings.EMAIL_HOST:
            self.stdout.write('Envoi test via SMTP...')
            try:
                send_mail(
                    'Test Riflet Automobile',
                    'E-mail de test depuis le serveur de production.',
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS('SMTP : envoyé'))
            except Exception as exc:
                self.stderr.write(self.style.ERROR(f'SMTP : échec — {exc}'))
        else:
            self.stderr.write(
                self.style.ERROR('Aucun canal e-mail actif (SMTP ou Resend).')
            )
