Social accounts
===============

AlekSIS can authenticate users against third party applications using OAuth2
or OpenID.

This can be used to grant access to persons whose credentials shall not be
managed in AlekSIS itself, for example because another authentication provider
is already used throughout the school, or for guardians that can or should for
some reason not get an LDAP account, or similar situations.

.. warning::
  Social accounts are **not** working with two factor authentication! If a user
  authenticates with a social account, the two factor authentication is
  ignored on login (but enforced for views that require two factor authentication later).

Configuring social account provider
-----------------------------------

For available providers, see documentation of `django-allauth
<https://django-allauth.readthedocs.io/en/latest/providers.html>`_.

A new social account provider can be configured in your configuration file
(located in ``/etc/aleksis/``).

Configuration example::

  [auth.providers.gitlab]
  GITLAB_URL = "https://gitlab.exmaple.com"

After configuring a new auth provider, you have to restart AlekSIS and configure client id and secret in the Backend Admin interface.
Click "Social applications" and add a new application. Choose your
provider and enter client id and secret from your application and choose
your site:

.. image:: ../_static/create_social_application.png
  :width: 100%
  :alt: Create social application
