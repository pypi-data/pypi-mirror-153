Background tasks
================

Operations that are expected to take a long time are run as background tasks.
For this, at least one `Celery`_ worker has to be running, e.g. by coupling it
with uWSGI as laid out in :ref:`core-configure-uwsgi`.

If a task is triggered from the AlekSIS frontend, for example by starting an import
job, a progress page is displayed, and the result of the job is waited for.

.. _core-periodic-tasks:

Periodic tasks
~~~~~~~~~~~~~~

Some tasks are also run on a schedule. For example, the backup job is run on
a regular basis.

All tasks in AlekSIS that are expected to run have a default schedule, which
is registered when migrating the database. Changing this default schedule
is currently only possible through the Django Admin backend, under
*Admin → Backend Admin*.

Under the *Periodic Tasks* app, you can define schedules and tasks. The names
of tasks you can add manually are documented in the respective sections
of the manual.
