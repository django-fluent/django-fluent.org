FROM python:3.6.1
MAINTAINER vdboor@edoburu.nl
ENV DEBIAN_FRONTEND=noninteractive \
    XDG_CACHE_HOME=/cache \
    PIP_CACHE_DIR=/cache/pip \
    PIP_NO_CACHE_DIR=off \
    PYTHONUNBUFFERED=1 \
    UWSGI_THREADS=5 \
    UWSGI_PROCESSES=2 \
    UWSGI_MODULE=djangofluent.wsgi.production:application \
    DJANGO_SETTINGS_MODULE=djangofluent.settings.production

RUN apt-get update && \
    apt-get install -y gettext && \
    rm -rf /var/lib/apt/lists/* /var/cache/debconf/*-old

# System setup
RUN useradd --system --user-group app
RUN pip install -U pip==9.0.1 setuptools==36.2.0 wheel==0.29.0

# Install dependencies
RUN mkdir -p /app/src/requirements
COPY src/requirements/*.txt /app/src/requirements/
ARG PIP_REQUIREMENTS=/app/src/requirements/docker.txt
RUN pip install -r $PIP_REQUIREMENTS

# Insert application code
ADD . /app/
WORKDIR /app/src
RUN rm /app/src/*/settings/local.py*
RUN find . -name '*.pyc' -delete && python -mcompileall -q */
RUN /app/src/manage.py compilemessages
RUN /app/src/manage.py collectstatic --noinput
RUN gzip --keep --best --force --recursive /app/web/static/
RUN mkdir -p /app/web/static/CACHE
RUN chown -R app:app /app/web/media/ /app/web/static/CACHE

# Create a default database inside the container (as demo),
# when caller doesn't define DATABASE_URL
ENV DATABASE_URL sqlite:////tmp/demo.db
RUN /app/src/manage.py migrate
RUN /app/src/manage.py loaddata example_data.json
RUN chown app:app /tmp/demo.db

# Insert main code (still as root)
COPY deployment/docker/uwsgi.ini /app/uwsgi.ini
CMD /usr/local/bin/uwsgi --ini /app/uwsgi.ini --procname-prefix-spaced "uwsgi: $UWSGI_MODULE"

# Expose
USER app
EXPOSE 8080
HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost:8080/api/ping/ || exit 1
VOLUME /app/web/media
