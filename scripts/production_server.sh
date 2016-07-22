#!/bin/sh

GUNICORN=/root/.virtualenvs/poke/bin/gunicorn
PROJECT_ROOT=/var/poke/pokemap

APP=wsgi:app

cd $PROJECT_ROOT
exec $GUNICORN -c $PROJECT_ROOT/config/gunicorn/guniconf.py $APP


