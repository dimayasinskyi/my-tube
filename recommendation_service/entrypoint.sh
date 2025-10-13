#!/bin/bash

echo "Creating superuser if not exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(username=username, password=password)
    print(f'Superuser {username} created.')

    token = Token.objects.create(user=user)
    print(f'Microservice token for user {username}: {token}')
else:
    User.objects.get(username=username)
    print(f'Superuser {username} already exists.')
"

exec gunicorn recommendation_service.wsgi:application --bind 0.0.0.0:8000