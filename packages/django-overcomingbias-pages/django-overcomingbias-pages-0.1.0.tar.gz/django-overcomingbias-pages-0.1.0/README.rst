django-overcomingbias-pages: a web interface to Robin Hanson's content
======================================================================

``django-overcomingbias-pages`` is a standalone `Django <https://www.djangoproject.com/>`_
app which provides a web interface to Robin Hanson's content.

Features
--------

The main features are:

- Scrape content from across the web (`overcomingbias <https://overcomingbias.com/>`_,
  `YouTube <https://www.youtube.com/>`_, `Spotify <https://spotify.com/>`_
  and more) via the admin site.

- Search content with
  `django-haystack <https://django-haystack.readthedocs.io/en/master/>`_.

- Create sequences (series) of content and export them to PDF, epub, plaintext,
  or any other format supported by `pandoc <https://pandoc.org/>`_.

- Persistent user accounts.

Configuration
-------------

To configure ``django-overcomingbias-pages``, add the following to your settings:

.. code-block:: python

  # settings.py

  # add required apps
  INSTALLED_APPS = [
    # required for admin site / user accounts
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # for collecting static files
    "django.contrib.staticfiles",
    # django-overcomingbias-api
    "ordered_model",
    "obapi",
    # haystack search
    "haystack",
    # async tasks
    "huey.contrib.djhuey",
    # django-overcomingbias-pages
    "obpages",
  ]

  # Use the (custom) obpages user model 
  AUTH_USER_MODEL = "obpages.User"


To configure search, follow the instructions on the
`haystack <https://django-haystack.readthedocs.io/en/master/>`_
doc pages.
If you don't care about search, just add this to your settings:

.. code-block:: python

  # settings.py

  # dummy backend for django-haystack
  HAYSTACK_CONNECTIONS = {
    "default": {
      "ENGINE": "haystack.backends.simple_backend.SimpleEngine",
    },
  }

``django-overcomingbias-pages`` uses `Huey <https://github.com/coleifer/huey>`_ to
run tasks asynchronously.
To enable this feature, follow the
`Django/Huey instructions <https://huey.readthedocs.io/en/latest/django.html>`_.
A minimal configuration is shown below:

.. code-block:: python

  # settings.py

  connection_pool = ConnectionPool(host="127.0.0.1", port=6379, db=0, max_connections=100)

  # See docs for full list of settings
  HUEY = {
      "huey_class": "huey.PriorityRedisHuey",
      "name": PROJECT_NAME,
      "connection": {
          "connection_pool": connection_pool,
          # see redis-py for more options
          # https://redis-py.readthedocs.io/en/latest/connections.html
          "read_timeout": 0,
      },
      "consumer": {
          "workers": 4,
          "worker_type": "thread",
      },
  }

(Note that this requires a Redis server running on localhost:6379.)

Optionally, you can also configure Huey as your
`email backend <https://github.com/chris-mcdo/django-huey-email-backend>`_.

Bugs/Requests
-------------

Please use the
`GitHub issue tracker <https://github.com/chris-mcdo/django-overcomingbias-pages/issues>`_
to submit bugs or request features.

License
-------

Copyright (c) 2022 Christopher McDonald

Distributed under the terms of the
`MIT <https://github.com/chris-mcdo/django-overcomingbias-pages/blob/main/LICENSE>`_
license.

All overcomingbias posts are copyright the original authors.
