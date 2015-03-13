django-fluent.org
=================

This is the source code of www.django-fluent.org
You can use this freely as example how to use and run a django-fluent CMS site.

Django Fluent CMS modules
-------------------------

The following modules are used in this site:

* `django-fluent-pages <https://github.com/edoburu/django-fluent-pages>`_
* `django-fluent-contents <https://github.com/edoburu/django-fluent-contents>`_
* `django-fluent-blogs <https://github.com/edoburu/django-fluent-blogs>`_
* `django-fluent-comments <https://github.com/edoburu/django-fluent-comments>`_
* `django-fluent-dashboard <https://github.com/edoburu/django-fluent-dashboard>`_
* `django-any-urlfield <https://github.com/edoburu/django-any-urlfield>`_
* `django-any-imagefield <https://github.com/edoburu/django-any-imagefield>`_
* `django-staff-toolbar <https://github.com/edoburu/django-staff-toolbar>`_

To create your own Django-Fluent project, use our template at:

https://github.com/edoburu/django-project-template

Project layout
--------------

This project uses the following layout:

* ``design/`` design source files
* ``src/`` all source code
* ``src/manage.py`` Django management tool
* ``src/Guardfile`` Guard configuration
* ``src/config.rb`` Compass configuration
* ``src/requirements.txt`` PIP requirements file
* ``src/apps/`` the Django apps.
* ``src/frontend/`` all frontend templates/JS/CSS code.
* ``src/djangofluent/`` The project folder with settings, WSGI hook and URLconf.
* ``src/djangofluent/settings/default.py`` configures default Django settings (same of all projects).
* ``src/djangofluent/settings/project.py`` the settings for this project.
* ``src/djangofluent/settings/local.py`` developer settings.
* ``src/djangofluent/settings/env/*.py`` settings per host (beta/production) and production DB credentials.
* ``src/djangofluent/wsgi/*.py`` WSGI start scripts per environment.
* ``src/djangofluent/urls.py`` top level URLconf.
* ``web/`` The public files exposed by the webserver.
* ``web/static/`` Static files by Django apps.
* ``web/media/`` Uploaded media files (JPG/PNG, etc..)


Local development
-----------------

Prerequisites
~~~~~~~~~~~~~

- Python >= 2.6
- pip
- virtualenv (virtualenvwrapper is recommended)

Installation
~~~~~~~~~~~~

To setup a local development environment::

    # Clone the repository
    git clone https://github.com/edoburu/django-fluent.org.git

    # Create the environment:
    mkvirtualenv django-fluent.org
    cd src
    pip install -r requirements.txt

    # Configure MySQL:
    mysql -u root -p
      create database `django-fluent.org`;
      grant all privileges on `django-fluent.org`.* to djangofluent@localhost identified by 'testtest';

    ./manage.py syncdb
    ./manage.py migrate

    # Start Django
    ./manage.py runserver

Compiling CSS files
~~~~~~~~~~~~~~~~~~~

To compile SASS_ files::

    gem install compass oily_png guard-livereload guard-compass

    guard

To enable LiveReload_ of ``*.css`` files during development, install a browser plugin:

* Firefox (2.0.9 dev release): https://github.com/siasia/livereload-extensions/downloads
* Everyone else: http://help.livereload.com/kb/general-use/browser-extensions

And toggle the "LiveReload" button in the browser at the desired page.

License
-------

Feel free to use parts of this code in your projects.

.. image::  http://i.creativecommons.org/l/by/3.0/88x31.png
   :target: http://creativecommons.org/licenses/by/3.0/
   :alt: Creative Commons License

Except otherwise noted, this project is © 2012-2013 Edoburu, under a `Creative Commons Attribution 3.0 Unported License <http://creativecommons.org/licenses/by/3.0/>`_.

The django-fluent modules are licensed under the Apache License Version 2.0.

The design is licensed from templatemo.com under a `Creative Commons Attribution 3.0 United States License <http://creativecommons.org/licenses/by/3.0/us/>`_.

Contributing
------------

Patches are welcome and gratefully accepted, for this site and everything else on our `GitHub page <https://github.com/edoburu>`_.


.. Add links here:

.. _Compass: http://compass-style.org/
.. _LiveReload: http://livereload.com/
.. _guard-livereload: https://github.com/guard/guard-livereload
.. _SASS: http://sass-lang.com/
