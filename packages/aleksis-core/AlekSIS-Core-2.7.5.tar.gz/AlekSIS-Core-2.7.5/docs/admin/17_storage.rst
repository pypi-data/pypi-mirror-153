Storage
=======

AlekSIS needs a writable storage, both for media files (pictures,
generated PDF files, and the like), and to store generated frontend
assets like the themed CSS stylesheet.

.. note::
    Everything except this media storage can be mounted and used
    entirely read-only, i.e. to keep the AlekSIS installation immutable.

Local filesystem storage
------------------------

By default, the media storage resides in the local filesystem, in the
location defined in the ``static.root`` configuration key.

.. warning::
    Do not expose the media storage directly through a webserver.
    AlekSIS uses a specially protected storage framework that
    employs cryptographic tokens to protect user data from URL
    guessing.

Amazon S3 (or other S#-compatible storage)
------------------------------------------

AlekSIS allows you to configure an Amazon S3 endpoint for  media
files. This is useful e.g. for loadbalancing with multiple AlekSIS
instances.

.. note::
   For some background jobs, AlekSIS stores HTML snippets in the media
   storage for later use. You must ensure your S3 endpoint is part of
   your ``Access-Control-Allow-Origin`` CORS header, so HTML loaded from
   there can load resources from the ALekSIS instance.

Configure an S3 endpoint
~~~~~~~~~~~~~~~~~~~~~~~~

If you want to use an S3 endpoint to store files you have to configure the
endpoint in your configuration file (`/etc/aleksis/aleksis.toml`)::

  # Default values
  [storage.s3]
  enabled = true
  endpoint_url = "https://minio.example.com"
  bucket_name = "aleksis-test"
  access_key_id = "XXXXXXXXXXXXXX"
  secret_key = "XXXXXXXXXXXXXXXXXXXXXX"
