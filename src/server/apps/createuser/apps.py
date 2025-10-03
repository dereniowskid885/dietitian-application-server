import os
from django.apps import AppConfig
from django.db import connections
from django.db.utils import OperationalError

class CreateUserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "server.apps.createuser"

    def ready(self):
        django_env = os.environ.get("DJANGO_ENV", "development")

        if django_env == "production":
            db_conn = connections['default']
            try:
                c = db_conn.cursor()
            except OperationalError:
                print("Baza danych nie jest jeszcze dostępna. Superuser nie zostanie utworzony.")
                return 

            from django.contrib.auth.models import User

            username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
            email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
            password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

            if username and password and not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
                print(f"Superuser '{username}' created.")
