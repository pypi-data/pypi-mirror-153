.. _core-data-checks:

Data checks
===========

Data checks are AlekSIS' mechanism for highlighting issues with the
contents of the database. These checks are not of a technical nature,
but strictly concern the contextual integrity of the data stored.


Verify data checks
------------------

In the menu under ``Admin → Data checks``, the status of all known
checks can be verified.

.. image:: ../_static/data_checks.png
   :width: 100%
   :alt: Data check overview

The first card shows the current global check state. If any data checks
reported issues, they will be listed here. In that case, administrators can
choose between options provided by the data checks to resolve the issues.

.. note::
   Details about the checks and solve options are described in the
   respective chapters of the manual.

Configure notifications
-----------------------

In the ``General`` tab of the configuration interface, you can configure
email notifications for problems detected by the data checks.

* General

  * Send emails if data checks detect problems: Enable email notifications
  * Email recipients for data checks problem emails: Choose recipient persons
  * Email recipient groups for data checks problem emails: Choose recipient groups

Data checks normally run once per hour, and if notifications are enabled, results
will be mailed to the selected recipients if problems are detected.
