#!/bin/sh

# just in case the db container is not ready to accept connections
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
# <module-that-contains-app>:<name-of-app>
exec gunicorn -b :5000 --access-logfile - --error-logfile - "chingu:create_app()"