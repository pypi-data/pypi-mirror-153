Registration and user invitations
=================================

In addition to central management of user accounts, AlekSIS allows self-registration
by users. Registration can be either fully open, or based on personal invitations.

In a system handling ciritcal data, access control should be as tight as possible.
However, there are scenarios where central account creation is not feasible, e.g.
for optional guardian accounts. In such a scenario, the invitation system allows
for processes like handing out invitation codes as a letter or through e-mail
campaigns.

Configuration
-------------

.. _core-registration:

Registration
~~~~~~~~~~~~

Registration can be enabled via the configuration interface in frontend.

In the ``Authentication`` tab, click the checkbox ``Enable signup`` to enable
signup for everyone. A menu item will be added for public registration.

.. warning::
   Do not enable this feature unless you intend to run a public AlekSIS instance.

User invitations
~~~~~~~~~~~~~~~~

.. _core-user-invitations:

In the same location as public registration, the invitation system can be enabled.

* Authentication

  * Enable invitations: Click to enable invitations.
  * Length of invite code: Length of invitation code packets, defaults to 5.
  * Size of packets: Configure how many packets are generated, defaults to 3.

By default, an invitation code looks like the following:
``abcde-abcde-abcde``.

A menu item will become available for users to enter their invitation code.

Usage
-----

Invite by email or code
~~~~~~~~~~~~~~~~~~~~~~~

To invite a new user , visit the invitation page located at ``People → Invite
person``

Here you are able to invite the user by email address or generate an
invitation code.

.. image:: ../_static/invitations.png
  :width: 100%
  :alt: Invitations page

This mechanism allows for registration of entirely new persons that do not
exist in the system, e.g. if perosnal details are not known in advance.

Invite existing person
~~~~~~~~~~~~~~~~~~~~~~

To invite an existing person, open the person in AlekSIS and click ``Invite
user``.

The invitation will be sent to the person's email address, and can only
be used by this person. Upon registration, the new account will automatically
be linked to the existing person.

.. image:: ../_static/invite_existing.png
  :width: 100%
  :alt: Invite existing person

.. note::
   Before using this feature, make sure to read and understand
   :ref:`core-concept-person`.
