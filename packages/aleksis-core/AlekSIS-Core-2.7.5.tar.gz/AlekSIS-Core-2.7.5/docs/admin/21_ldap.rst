.. _core-ldap:

Authenticating against LDAP
===========================

AlekSIS can authenticate users against an LDAP directory (like OpenLDAP or
Active Directory). The AlekSIS core can only authenticate and synchronise
authenticated users to AlekSIS’ database. There are apps that help with
tasks like mass-importing accounts and linking accounts to persons in
the AlekSIS system (see below).


Installing packages for LDAP support
------------------------------------

Installing the necessary librairies for LDAP support unfortunately is not
very straightforward under all circumstances. On Debian, install these packages::

  sudo apt install python3-ldap libldap2-dev libssl-dev libsasl2-dev python3-dev


Configuration of LDAP support
-----------------------------

Configuration is done under the ``ldap`` section in AlekSIS’
configuration file. For example, add something like the following to your
configuration (normally in ``/etc/aleksis``; you can either append to an
existing file or add a new one)::

  [ldap]
  uri = "ldaps://ldap.myschool.edu"
  bind = { dn = "cn=reader,dc=myschool,dc=edu", password = "secret" }

  [ldap.users]
  search = { base = "ou=people,dc=myschool,dc=edu", filter = "(uid=%(user)s)" }
  map = { first_name = "givenName", last_name = "sn", email = "mail" }

  [ldap.groups]
  search = { base = "ou=groups,dc=myschool,dc=edu" }
  type = "groupOfNames"
  # Users in group "admins" are superusers
  flags = { is_superuser = "cn=admins,ou=groups,dc=myschool,dc=edu" }
