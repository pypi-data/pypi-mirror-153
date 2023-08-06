Mail
====

AlekSIS needs to send mails e.g. for account confirmations, feedback or
error reports.

Configure mailing
-----------------

The mailserver can be configured via the configuration file

.. code-block:: toml

	[mail.server]
	host = "mail.example.com"
	tls = False
	ssl = True
	port = 25
	user = "mailuser"
	password = "password"

Name and address for mails sent by AlekSIS can be configured in the
webinterface.  To configure, visit `Admin → Configuration` and click on the
`Mail` tab.

Configure mail recipients
-------------------------

You can configure admin contacts in your configuration file, located at
``/etc/aleksis/``.

.. code-blocK:: toml

	[contact]
	admins = [["AlekSIS - Admins", "root@example.com"],["AlekSIS - Admins2", "root2@example.com"]]
	from = 'aleksis@example.com'
