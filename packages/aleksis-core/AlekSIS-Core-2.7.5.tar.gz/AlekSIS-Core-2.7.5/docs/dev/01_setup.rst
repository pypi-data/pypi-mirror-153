Setting up the development environment
======================================

AlekSIS and all official apps use `Poetry`_ to manage virtualenvs and
dependencies. You should make yourself a bit confortable with poetry
by reading its documentation.

Poetry makes a lot of stuff very easy, especially managing a virtual
environment that contains AlekSIS and everything you need to run the
framework and selected apps.

Also, `Yarn`_ is needed to resolve JavaScript dependencies.

For repository management, `myrepos` is required.

Setup database and message broker
---------------------------------

AlekSIS requires `PostgreSQL`_ (version 13 or newer) as database
backend. To provide a database names `aleksis` with a user named
`aleksis` on Debian::

  sudo apt install postgresql
  sudo -u postgres createuser -P aleksis
  sudo -u postgres createdb -O aleksis aleksis

Additionally, `Redis`_ is used as message broker and for caching.
The default configuration of the server in Debian is sufficient::

  sudo apt install redis-server

Get the source tree
-------------------

To download AlekSIS and all officially bundled apps in their
development version, use Git like so::

  git clone https://edugit.org/AlekSIS/official/AlekSIS

This first downloads a meta repository that contains a config file for mr.
To clone the AlekSIS-Core and all official (and onboarding) apps, run::

  mr update

Install native dependencies
---------------------------

Some system libraries are required to install AlekSIS. On Debian, for example, this would be done with::

  sudo apt install build-essential libpq-dev libpq5 libssl-dev python3-dev python3-pip python3-venv yarnpkg gettext chromium

Get Poetry
----------

Make sure to have Poetry installed like described in its
documentation. Right now, we encourage using pip to install Poetry
once system-wide (this will change once distributions pick up
Poetry).::

  sudo pip3 install poetry

You can use any other of the `Poetry installation methods`_.


Install AlekSIS in its own virtual environment
----------------------------------------------

Poetry will automatically manage virtual environments per project, so
installing AlekSIS is a matter of switching into the Core's directory and running the initial AlekSIS installation::

  cd apps/official/AlekSIS-Core
  poetry install

Now it's recommended to run a shell that uses the newly created venv::

  poetry shell


Regular tasks
-------------

After making changes to the environment, e.g. installing apps or updates,
some maintenance tasks need to be done:

1. Download and install JavaScript dependencies
2. Collect static files
3. Run database migrations

All three steps can be done with the ``poetry shell`` command and
``aleksis-admin``::

  ALEKSIS_maintenance__debug=true ALEKSIS_database__password=aleksis poetry shell
   poetry run aleksis-admin yarn install
   poetry run aleksis-admin collectstatic
   poetry run aleksis-admin compilemessages
   poetry run aleksis-admin migrate
   poetry run aleksis-admin createinitialrevisions

Running the development server
------------------------------

The development server can be started using Django's ``runserver`` command.
If you want to automatically start other necessary tools in development,
like the `Celery`_ worker and scheduler, use ``runuwsgi`` instead.
You can either configure AlekSIS like in a production environment, or pass
basic settings in as environment variable. Here is an example that runs the
development server against a local PostgreSQL database with password
`aleksis` (all else remains default) and with the `debug` setting enabled::

  ALEKSIS_maintenance__debug=true ALEKSIS_database__password=aleksis poetry run aleksis-admin runuwsgi

.. _Poetry: https://poetry.eustace.io/
.. _Poetry installation methods: https://poetry.eustace.io/docs/#installation
.. _Yarn: https://yarnpkg.com
.. _PostgreSQL: https://www.postgresql.org/
.. _Redis: https://redis.io/
.. _Celery: https://celeryproject.org/
