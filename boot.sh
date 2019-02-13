#!/bin/sh

source venv/bin/activate
flask db upgrade
# <module-that-contains-app>:<name-of-app>
exec gunicorn -b :5000 --access-logfile - --error-logfile - "chingu.__init__:create_app()"