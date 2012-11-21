www.django-fluent.org
=====================

This is the source code of www.django-fluent.org
You can use this freely as example how to use and run a django-fluent CMS site.

Installation
------------

* Clone this repository

::

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

