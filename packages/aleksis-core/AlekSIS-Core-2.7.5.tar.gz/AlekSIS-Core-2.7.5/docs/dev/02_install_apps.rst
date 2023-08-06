Installing apps into development environment
============================================

Officially bundled apps
-----------------------

Officially bundled apps are available in the ``apps/official/``
sub-folder of the meta repository. If you followed the documentation, they
will already be checked out in the version required for the bundle you
are running.

Installing a development environment for own apps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are developing your own app, you probably do not want to
ru na development environment from the `AlekSIS-Core` repository.

Instead, simply install the environment using ``poetry install`` from
your app repository – it will pull in `AlekSIS-Core` as a dependency
automatically, and everything will work as described beforehand.

.. note::
   Take care not to mix up environments, especially if using ``poetry shell``.


Using one virtual environment for everything
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
   This method is not encouraged for most use cases.

Installing apps into the existing virtual environment of `AlekSIS-Core` can
be easily done after starting `poetry shell`::

  poetry install

Do not forget to run the maintenance tasks described earlier after
installing any app.

.. note::
   This is not suitable for working on the core, because it
   will install the `AlekSIS-Core` version used by the app using `pip` again.
