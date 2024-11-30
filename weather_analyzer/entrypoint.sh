#!/bin/bash

echo "Running makemigrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

echo "Starting the Django app..."
python manage.py runserver 0.0.0.0:8000