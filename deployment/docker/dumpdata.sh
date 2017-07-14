#!/bin/sh
container_id="$(docker ps -qf 'ancestor=django-fluent.org:latest')"
if [ -z "$container_id" ]; then
  echo "No container ID found for django-fluent.org, is the image running?" >&2
  exit 1
fi

cd $(dirname $0)/../..
docker exec -it "$container_id" /app/src/manage.py dumpdata --indent=2 --natural-foreign --exclude=admin --exclude=contenttypes --exclude=auth.permission --exclude=sessions --exclude=filebrowser  > src/example_data2.json
