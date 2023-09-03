#!/bin/bash

# echo "Apply Migrations"

echo "Migrate"

python ./django_backend/manage.py migrate

echo "Create Superuser"

echo "from django.contrib.auth import get_user_model; import os; User = get_user_model(); User.objects.create_superuser('admin', 'raimundo@hotmail.com', 'raimu123'); print('superuser created.')" | python ./django_backend/manage.py shell

echo "from api.models import ProposalModel; ProposalModel.objects.create(); print('Proposal model created.')" | python ./django_backend/manage.py shell


echo "Make Migrations"
python ./django_backend/manage.py makemigrations
python ./django_backend/manage.py migrate

exec "$@"
