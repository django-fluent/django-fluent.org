# Build environment has gcc and develop header files.
# The installed files are copied to the smaller runtime container.
FROM python:3.8-buster as build-image
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off

# Install (and compile) all dependencies
RUN mkdir -p /app/src/requirements
COPY src/requirements/*.txt /app/src/requirements/
ARG PIP_REQUIREMENTS=/app/src/requirements/docker.txt
RUN pip install -r $PIP_REQUIREMENTS

# Remove unneeded files
RUN find /usr/local/lib/python3.8/site-packages/ -name '*.po' -delete && \
    find /usr/local/lib/python3.8/site-packages/tinymce/ -regextype posix-egrep -not -regex '.*/langs/(en|nl).*\.js' -wholename '*/langs/*.js' -delete

## Node builder
FROM node:14-buster as frontend-build
RUN mkdir -p /app/src
WORKDIR /app/src
COPY src/package.json src/package-lock.json /app/src/
RUN npm install
COPY src/gulpfile.js /app/src/
COPY src/frontend/ /app/src/frontend/
RUN npm run gulp

# Start runtime container
FROM python:3.8-slim-buster
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    UWSGI_PROCESSES=1 \
    UWSGI_THREADS=10 \
    UWSGI_OFFLOAD_THREADS=1 \
    UWSGI_MODULE=djangofluent.wsgi.docker:application \
    DJANGO_SETTINGS_MODULE=djangofluent.settings.docker

# Install runtime dependencies (can become separate base image)
# Also include gettext for now, so locale is still compiled here.
# It avoids busting the previous cache layers on code changes.
RUN apt-get update && \
    mkdir -p /usr/share/man/man1 /usr/share/man/man5 /usr/share/man/man7 /usr/share/man/man8 && \
    apt-get install --no-install-recommends -y \
        libxml2 \
        libpng16-16 \
        libopenjp2-7 \
        libfreetype6 \
        libtiff5 \
        curl \
        gettext \
        mime-support \
        postgresql-client && \
    rm -rf /var/lib/apt/lists/* /var/cache/debconf/*-old && \
    echo "font/woff2  woff2" >> /etc/mime.types && \
    useradd --system --user-group app

# System config (done early, avoid running on every code change)
MAINTAINER vdboor@edoburu.nl
EXPOSE 8080 1717
HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost:8080/api/health/ || exit 1

# Install dependencies
COPY --from=build-image /usr/local/bin/ /usr/local/bin/
COPY --from=build-image /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=frontend-build /app/src/frontend/static /app/src/frontend/static

# Insert application code.
# - Prepare gzipped versions of static files for uWSGI to use
# - Create a default database inside the container (as demo),
#   when caller doesn't define DATABASE_URL
# - Give full permissions, so Kubernetes can run the image as different user
ENV DATABASE_URL=sqlite:////tmp/demo.db
COPY web /app/web
COPY src /app/src
COPY deployment/docker/manage.py /usr/local/bin/
WORKDIR /app/src
RUN rm /app/src/*/settings/local.py* && \
    find . -name '*.pyc' -delete && \
    python -mcompileall -q */ && \
    manage.py compilemessages && \
    manage.py collectstatic --noinput --link && \
    manage.py migrate && \
    manage.py loaddata example_data.json && \
    mkdir -p /app/web/media /app/web/static/CACHE && \
    chown -R app:app /app/web/media/ /app/web/static/CACHE /tmp/demo.db && \
    chmod -R go+rw /app/web/media/ /app/web/static/CACHE /tmp/demo.db

# Insert main code (still as root), then reduce permissions
# Allow to mount the compressor cache as volume too for sharing between pods.
COPY deployment/docker/uwsgi.ini /app/uwsgi.ini
CMD ["/usr/local/bin/uwsgi", "--ini", "/app/uwsgi.ini"]
VOLUME /app/web/media
VOLUME /app/web/static/CACHE

# Tag the docker image
ARG GIT_VERSION
LABEL git-version=$GIT_VERSION
RUN echo $GIT_VERSION > .docker-git-version

# Reduce default permissions
USER app
