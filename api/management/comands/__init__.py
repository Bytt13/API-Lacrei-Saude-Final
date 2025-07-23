import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USER")
        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")

        # Verifica se todas as etiquetas necessárias foram fornecidas
        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR())
            return

        # Verifica se o gerente já foi contratado para não o criar duas vezes
        if not User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f"Criando superusuário: {username}"))
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(self.style.SUCCESS("Superusuário criado com sucesso!"))
        else:
            self.stdout.write(
                self.style.WARNING(f"O superusuário {username} já existe.")
            )
