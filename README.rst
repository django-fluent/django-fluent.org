django-fluent.org
=================

This is the source code of www.django-fluent.org
You can use this freely as example how to use and run a django-fluent CMS site.

Prerequisites
-------------

- Python >= 2.6
- pip
- virtualenv (virtualenvwrapper is recommended)

Installation
------------

To setup a local development environment::

    # Clone the repository
    git clone https://github.com/edoburu/django-fluent.org.git

    # Create the environment:
    mkvirtualenv django-fluent.org
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

    gem install compass bootstrap-sass oily_png guard-livereload guard-compass

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
