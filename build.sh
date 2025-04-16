#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser
echo "from django.contrib.auth.models import User; User.objects.create_superuser('baihelahusain', 'baihelahusain@gmail.com', 'bah@7865354') if not User.objects.filter(username='baihelahusain').exists() else None" | python manage.py shell 