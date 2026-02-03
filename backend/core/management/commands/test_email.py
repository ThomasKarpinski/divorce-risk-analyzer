from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import smtplib

class Command(BaseCommand):
    help = 'Test email sending'

    def handle(self, *args, **kwargs):
        self.stdout.write(f"Attempting to send email...")
        self.stdout.write(f"FROM: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"HOST: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        self.stdout.write(f"USER: {settings.EMAIL_HOST_USER}")
        key_len = len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 0
        self.stdout.write(f"KEY LENGTH: {key_len}")

        try:
            send_mail(
                'Test Subject',
                'This is a test email from your Django app.',
                settings.DEFAULT_FROM_EMAIL,
                ['tomaszkarpinski204@gmail.com'],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('Email sent successfully!'))
        except smtplib.SMTPResponseException as e:
            self.stdout.write(self.style.ERROR(f'SMTP Error: {e.smtp_code} - {e.smtp_error}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'General Error: {str(e)}'))
