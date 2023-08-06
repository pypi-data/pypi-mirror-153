Merging of app settings
=======================

AlekSIS provides features to merge app settings into main ``settings.py``.

Currently mergable settings
---------------------------

 * INSTALLED_APPS
 * DATABASES
 * YARN_INSTALLED_APPS
 * ANY_JS

If you want to add another database for your AlekSIS app, you have to add
the following into your ``settings.py``::

    DATABASES = {
        "database": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "database",
            "USER": "database",
            "PASSWORD": "Y0urV3ryR4nd0mP4ssw0rd",
            "HOST": "127.0.0.1",
            "PORT": 5432,
        }
