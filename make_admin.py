import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User

username = 'skywalker'
password = 'iphone16promaxtop'
email = 'admin@example.com'

User.objects.filter(username=username).delete()
User.objects.create_superuser(username, email, password)
print(f'Админ {username} создан!')
