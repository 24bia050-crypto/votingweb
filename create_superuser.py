import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voting_project.settings")
django.setup()

from django.contrib.auth.models import User

username = "user"
email = "24bia050@gmail.com"
password = "Admin123456"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("Superuser created")
else:
    print("Superuser already exists")