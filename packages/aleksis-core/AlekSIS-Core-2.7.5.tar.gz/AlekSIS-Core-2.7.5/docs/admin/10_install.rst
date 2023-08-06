Install AlekSIS
===============

From PyPI
---------

In this section we will install AlekSIS with `uWSGI` and `nGINX` on Debian
bullseye.

Filesystem locations
~~~~~~~~~~~~~~~~~~~~

AlekSIS will need and use the following paths:

 * `/etc/aleksis` for configuration files
 * `/var/lib/aleksis/media` for file storage (Django media)
 * `/var/backups/aleksis` for backups of database and media files
 * `/usr/local/share/aleksis/static` for static files
 * `/usr/local/share/aleksis/node_modules` for frontend dependencies

You can change any of the paths as you like.

.. _core-install-prerequisites:

Prerequisites
~~~~~~~~~~~~~

For an installation on a dedicated server, the following prerequisites are needed:

 * Debian 11
 * PostgreSQL
 * Redis
 * uWSGI
 * nginx
 * Python 3.9
 * Some system dependencies to build Python modules and manage frontend files
 * The aforementioned paths

Install system packages
~~~~~~~~~~~~~~~~~~~~~~~

Install some packages from the Debian package system.

.. code-block:: shell

   apt install uwsgi \
               uwsgi-plugin-python3 \
               nginx-full \
               python3 \
               python3-dev \
               libpq-dev \
               yarnpkg \
               python3-virtualenv \
               chromium \
               redis-server \
               postgresql

Create PostgreSQL user and database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate a secure password for the database, then create the user and database.

.. code-block:: shell

   sudo -u postgres createuser -D -P -R -S aleksis
   sudo -u postgres createdb -E UTF-8 -O aleksis -T template0 -l C.UTF-8 aleksis

When asked, use the password generated above.

Create the directories for storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

   mkdir -p /etc/aleksis \
            /usr/share/aleksis/{static,node_modules} \
            /var/lib/aleksis/media \
            /var/backups/aleksis
   chown -R www-data:www-data /var/lib/aleksis

Create AlekSIS configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AlekSIS is configured in files in `/etc/aleksis`. Create a basic configuration file
for the environment defined above by opening `/etc/aleksis/aleksis.toml` with your
favourite text editor and adding the following configuration.

.. code-block:: toml

   static = { root = "/usr/local/share/aleksis/static", url = "/static/" }
   media = { root = "/var/lib/aleksis/media", url = "/media/" }
   node_modules = { root = "/usr/local/share/aleksis/node_modules" }
   secret_key = "SomeRandomValue"

   [http]
   allowed_hosts = ["aleksis.example.com"]

   [database]
   host = "localhost"
   name = "aleksis"
   username = "aleksis"
   password = "password_generated_above"

   [backup]
   location = "/var/backups/aleksis"

   [auth.superuser]
   username = "admin"
   password = "admin"
   email = "root@localhost"

Install AlekSIS itself
~~~~~~~~~~~~~~~~~~~~~~

To install AlekSIS now, and run all post-install tasks, run the following commands.
They will pull the AlekSIS standard distribution from `PyPI`_ and install it to the
system-wide `dist-packages` of Python. Afterwards, it will download frontend dependencies
from `yarnpkg`, collect static files, and migrate the database to the final schema.

.. code-block:: shell

   pip3 install aleksis
   aleksis-admin yarn install
   aleksis-admin collectstatic
   aleksis-admin migrate
   aleksis-admin createinitialrevisions

.. _core-configure-uwsgi:

Configure uWSGI
~~~~~~~~~~~~~~~

uWSGI is an application server that will manage the server processes and requests.
It will also run the Celery broker and scheduler for you.

Configure a uWSGI app by opening `/etc/uwsgi/apps-available/aleksis.ini` in an
editor and inserting:

.. code-block:: toml

   [uwsgi]
   vhost = true
   plugins = python3
   master = true
   enable-threads = true
   processes = 20
   wsgi-file = /usr/local/lib/python3.9/dist-packages/aleksis/core/wsgi.py
   chdir = /var/lib/aleksis
   lazy = true
   lazy-apps = true
   attach-daemon = celery -A aleksis.core worker --concurrency=4
   attach-daemon = celery -A aleksis.core beat

Afterwards, enable the app using:

.. code-block:: shell

   ln -s /etc/uwsgi/apps-available/aleksis.ini /etc/uwsgi/apps-enabled/aleksis.ini
   service uwsgi restart

Configure the nginx webserver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, you should get a TLS certificate, e.g. by using `Let's Encrypt`_.

Then, create a virtual host in nginx, by editing `/etc/nginx/sites-available/aleksis.example.com`.

.. code-block:: nginx

   upstream aleksis {
     server unix:///run/uwsgi/app/aleksis/socket;
   }

   server {
     listen 80;
     listen [::]:80;

     server_name aleksis.example.com;

     return 301 https://$server_name$request_uri;
   }

   server {
     listen 443 ssl http2;
     listen [::]:443 ssl http2;

     ssl_certificate /etc/letsencrypt/certs/aleksis.example.com/fullchain.pem;
     ssl_certificate_key /etc/letsencrypt/certs/aleksis.example.com/privkey.pem;
     ssl_trusted_certificate /etc/letsencrypt/certs/aleksis.example.com/chain.pem;

     server_name aleksis.example.com;

     access_log /var/log/nginx/access.log;

     location /static {
       alias /usr/local/share/aleksis/static;
     }

     location / {
       uwsgi_pass aleksis;
       include uwsgi_params;
       proxy_redirect off;
       proxy_pass_header Authorization;
     }
   }

Enable the virtual host:

.. code-block:: shell

   ln -s /etc/nginx/sites-available/aleksis.example.com /etc/nginx/sites-enabled/aleksis.example.com
   service nginx restart

Finalisation
~~~~~~~~~~~~

Your AlekSIS installation should now be reachable and you can login with the administration
account configured above.

With Docker
-----------

AlekSIS can also be installed using Docker, either only AlekSIS itself, or the
full stack, including Redis, using docker-compose

Full stack using docker-compose
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, install Docker and docker-compose on your system. Also install git
to get the docker-compose file and image definition.

.. code-block:: shell

   apt install docker.io docker-compose git

Now, clone the distribution repository, which contains the docker-compose
file.

.. code-block:: shell

   git clone https://edugit.org/AlekSIS/official/AlekSIS

You should review the file `docker-compose.yaml` for any environment variables
you want to change.

Finally, bring the stack up using:

.. code-block:: shell

  docker-compose up -d

AlekSIS will be reachable on port 80 if you forgot to configure the environment.
You are responsible for adding a reverse proxy like nginx providing TLS, etc.

.. _Dynaconf: https://dynaconf.readthedocs.io/en/latest/
.. _Let's Encrypt: https://certbot.eff.org/instructions
.. _PyPI: https://pypi.org
