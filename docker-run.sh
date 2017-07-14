#!/bin/sh
docker run --rm -p 8080:8080 -e DJANGO_SETTINGS_MODULE=djangofluent.settings -it django-fluent.org:latest
