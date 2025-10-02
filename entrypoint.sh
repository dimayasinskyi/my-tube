#!/bin/sh

gunicorn --chdir /usr/src/app/recommendation_service recommendation_service.wsgi:application --bind 127.0.0.1:7000 &
MICROSERVICE_PID=$!
echo "Recommendation_service is working!"

sleep 3

python /usr/src/app/mytube/manage.py collectstatic --noinput
exec gunicorn --chdir /usr/src/app/mytube mytube.wsgi:application --bind 0.0.0.0:8000 &
WEB_PID=$!
echo "Project is running"

while true; do
    for pid in $WEB_PID $MICROSERVICE_PID; do
        if ! kill -0 $pid 2>/dev/null; then
            EXIT_CODE=1
            echo "Process $pid exited. Stopping others..."
            kill -TERM $WEB_PID $MICROSERVICE_PID 2>/dev/null || true
            exit $EXIT_CODE
        fi
    done
    sleep 1
done
