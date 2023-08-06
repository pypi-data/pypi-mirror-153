Configuration options
=====================

AlekSIS provides lots of options to configure your instance.

Configuration file
------------------

All settings which are required for running an AlekSIS instance are stored in your configuration file ``/etc/aleksis/aleksis.toml``.

Example configuration file::

    # General config for static, media and secret key, required
    static = { root = "/srv/www/aleksis/data/static", url = "/static/" }
    media = { root = "/srv/www/aleksis/data/media", url = "/media/" }
    secret_key = "Xoc8eiwah3neehid2Xi3oomoh4laem"

    # Admin contat, optional
    [contact]
    admins = [["AlekSIS - Admins", "root@example.com"]]
    from = 'aleksis@example.com'

    # Allowed hosts, required
    [http]
    allowed_hosts = ["localhost"]

    # Database for whole AlekSIS data, required
    [database]
    host = "localhost"
    name = "aleksis"
    username = "aleksis"
    password = "aleksis"

    # Maintenance mode and debug, optional
    [maintenance]
    debug = true

    # Two factor authentication with yubikey enabled, optional
    [2fa]
    enabled = true
    yubikey = { enabled = true }

    # Authentication via LDAP, optional
    [ldap]
    uri = "ldaps://ldap.myschool.edu"
    bind = { dn = "cn=reader,dc=myschool,dc=edu", password = "secret" }
    map = { first_name = "givenName", last_name = "sn", email = "mail" }

    [ldap.users]
    search = { base = "ou=people,dc=myschool,dc=edu", filter = "(uid=%(user)s)" }

    [ldap.groups]
    search = { base = "ou=groups,dc=myschool,dc=edu" }
    type = "groupOfNames"
    # Users in group "admins" are superusers
    flags = { is_superuser = "cn=admins,ou=groups,dc=myschool,dc=edu" }

    # Search index, optional
    [search]
    backend = "whoosh"
    index = "/srv/www/aleksis/data/whoosh_index"

Configuration in frontend
-------------------------

Everything that does not have to be configured before the AlekSIS instance fully starts can be configured in frontend, such as site title and logo.

You can find the configuration options in your AlekSIS instance under ``Admin → Configuration``.
