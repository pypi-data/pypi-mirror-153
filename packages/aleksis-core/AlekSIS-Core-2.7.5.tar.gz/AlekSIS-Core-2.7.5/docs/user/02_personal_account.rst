Managing your personal account
==============================

Each logged in user has several options to provided through the AlekSIS
core. Which of these items are display depends on whether the user has a
person and what your system administrator has configured.

.. _core-notifications:

Notifications
-------------

The AlekSIS core has a built-in notification system which can be used by
apps to send urgent information to specific persons (e. g. timetable
changes). Notifications are shown on the dashboard and the notifications
page reachable over the menu entry ``Notifications``. In addition to
that, notifications can be sent to users through several communication
channels. These channels can be switched on or off in your personal
preferences (cf. :ref:`core-user-preferences`).

Setup two-factor authentication
-------------------------------


.. image:: ../_static/2fa.png
  :width: 100%
  :alt: Configure two factor authentication

AlekSIS provides two factor authentication using hardware tokens such as
yubikeys which can generate OTPs or OTP application.

To configure the second factor, visit `Account → 2FA` and follow the
instructions.

Please keep the backup codes somewhere safe so you do not lose access to
your account. If you are unable to login with two factor authentication,
please contact your site administrator.

If you forget to safe your backup codes, but you are still logged in, visit
`Account → 2FA`, and press `Show codes`.

To disable two factor authentication, login to your account and navigate to
`Account → 2FA`, then press the big red button to disable 2fa.

Change password
---------------

If your system administrator has activated this function, you can change
your password via ``Account → Change password``. If you forgot your
password, there is a link ``Password forgotten?`` on this page which
helps with resetting your password. The system then will send you a
password reset link via email.

Me page
-------

Reachable under ``Account → Me``, this page shows the personal
information saved about you in the system. If activated, you can upload
a picture of yourself or edit some information.

.. _core-user-preferences:

Personal preferences
--------------------

You can configure some behavior using the preferences under
``Account → Preferences``. By default, the Core only provides some
preferences, but apps can extend this list. You can find further
information about such preferences in the chapter of the respective
apps.

-  **Notifications**

   -  **Name format for addressing**: Here you can select how AlekSIS
      should address you.
   -  **Channels to use for notifications:** This channel is used to
      sent notifications to you (cf. :ref:`core-notifications`).

Third-party accounts
--------------------

If you logged in using a third-party account (e. g. a Google or
Microsoft account), you can manage the connections to these accounts on
the page ``Account → Third-party accounts``.

The feature to use third-party accounts needs to be enabled by
an administrator, as described in :doc:`../admin/04_socialaccounts`.

Authorized applications
-----------------------

On the page ``Account → Authorized applications`` you can see all
external applications you authorized to retreive data about you from
AlekSIS. That can be services provided by your local institution like a
chat platform, for example.
