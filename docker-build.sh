#!/bin/sh

cd $(dirname $0)
docker build -t django-fluent.org .
