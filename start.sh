#!/usr/bin/env bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn suivi_des_investisseur.wsgi:application