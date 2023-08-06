Providing important information to users using the dashboard
============================================================

The dashboard is a central place for providing important information to users.
This is done by so-called dashboard widgets provided by the Core and apps.

Built-in dashboard widgets
--------------------------

External link widget
^^^^^^^^^^^^^^^^^^^^

The external link widget will show a link to an external site on the dashboard,
optionally with an icon or picture next to it. It therefore provides the following additional attributes:

* **URL**: The URL of the external site.
* **Icon URL**: The URL of the icon or picture shown next to the link.

As link title, the widget title will be used.

More dashboard widgets from apps
--------------------------------

In addition to the built-in widgets, apps can provide their own dashboard widgets.
Best examples for such apps are currently *AlekSIS-App-DashboardFeeds* and *AlekSIS-App-Chronos*.

.. Add References to the apps

.. _core-configure-dashboard-widgets:

Add and configure dashboard widgets
-----------------------------------

If you want to add a new dashboard widget, you can do so by adding the dashboard widget at *Admin → Dashboard widgets*.
There you will see all currently configured dashboard widgets and
can add new ones using the *Create dashboard widget* button which will ask your for the widget type.

.. image:: ../_static/dashboard_widgets.png
  :width: 100%
  :alt: All configured dashboard widgets

Each dashboard widget has at least the followong attributes

* **Widget Title**: The title of the widget (will be shown in some widgets).
* **Activate Widget**: If this isn't checked, the widget will not be shown.
* **Widget is broken**: If this is checked, the widget will be shown
  but the user will get a message that this widget is currently out of order because of an error.
  This shouldn't be checked by yourself, but might be activated automatically by a widget if it encounters an error.
  If this case enters, you should check for the cause of the error and fix it. After that, you can unmark the widget as broken.
* **Size on different screens**: The size of the widget on different screens.
  We work with a grid system containing a maximum of 12 columns. So, one column is 1/12 of the screen width.
  The width in the following fields has to be entered as number of columns (1 to 12).

  * **Size on mobile devices**: The size of the widget on mobile devices (600px and less).
  * **Size on tablet devices**: The size of the widget on desktop devices (600px - 992px).
  * **Size on desktop devices**: The size of the widget on desktop devices (992px - 1200px).
  * **Size on large desktop devices**: The size of the widget on large desktop devices (1200px and above).

All other attributes are specific to the widget type and are explained in the documentation of the widget.

.. image:: ../_static/create_dashboard_widget.png
  :width: 100%
  :alt: Form to create an external link widget

Setup a default dashboard
-------------------------

To make the configured dashboard widgets accessible to all users, we recommend to configure the default dashboard.
If you don't do so, the dashboard widgets will only be available to users if they customise their dashboard.

The default dashboard can be configured via *Admin → Dashboard widgets → Edit default dashboard*.
The edit page works exactly as the page described in :ref:`core-user-customising-dashboard`.

.. image:: ../_static/edit_default_dashboard.png
  :width: 100%
  :alt: Edit the default dashboard

Preferences
-----------

The behavior of the dashboard can be configured via *Admin → Configuration → General*. The following settings are available:

* **Show dashboard to users without login**: If this is checked, the dashboard will be also shown to users who are not logged in.

.. warning::

    That won't work with all dashboard widgets. Some widgets, like the timetable widgets, require a logged in user.

* **Allow users to edit their dashboard**: With this preference, system administrators can decide whether users
  can edit their own dashboard as described in :ref:`core-user-customising-dashboard`.
* **Automatically update the dashboard and its widgets sitewide**: If enabled,
  the dashboard will be updated automatically every 15 seconds.
