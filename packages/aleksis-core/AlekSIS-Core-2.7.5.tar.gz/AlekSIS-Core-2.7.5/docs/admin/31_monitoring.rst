.. _sec:Monitoring:

Monitoring and health checks
============================

Configuration
-------------

Thresholds
~~~~~~~~~~

Thresholds for health checks can be configured via config file
(``/etc/aleksis``).

.. code:: toml

   [health]
   disk_usage_max_percent = 90
   memory_min_mb = 500

   [backup.database]
   check_seconds = 7200

   [backup.media]
   check_seconds = 7200

Status page
-----------

AlekSIS' status page shows information about the health of your AlekSIS
instance. You can visit it via the left navigation bar (Admin → Status).

The page shows information about debug and maintenance mode, a summary of
your health checks and the last exit status of your celery tasks. This
page can not be used as a health check, it will always return HTTP 200
if the site is reachable.

Health check
------------

The health check can be used to verify the health of your AlekSIS
instance. You can access it via the browser
(https://aleksis.example.com/health/) and it will show you a summary of
your health checks. If something is wrong it will return HTTP 500.

It is also possible to get a JSON response from the health check, for
example via ``curl``. You only have to pass a valid
``Accept: application/json`` header to your request.

The health check can also be executed via ``aleksis-admin``:

.. code:: shell

   $ aleksis-admin health_check

Monitoring with Icinga2
-----------------------

As already mentioned, there is a JSON endpoint at
https://aleksis.example.com/health/. You can use an json check plugin to
check seperate health checks or just use a HTTP check to check if the
site returns HTTP 200.

Performance monitoring with Prometheus
--------------------------------------

AlekSIS provides a Prometheus exporter. The exporter provides metrics
about responses and requests, e.g. about response codes, request
latency and requests per view. It also provides data about database
operations.

The metrics endpoint can be found at
https://aleksis.example.com/metrics. In the default configuration it can
be scraped from everywhere. You might want to add some webserver
configuration to restrict access to this url.

To get metrics of your AlekSIS instance, just add the following to
``prometheus.yml``

.. code:: yaml

     - job_name: aleksis
       static_configs:
         - targets: ['aleksis.example.com']
       metrics_path: /metrics

Rules for prometheus alertmanager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are using the prometheus alertmanager, it is possible to create
some alerting rules so that an alert is fired when your AlekSIS instance
is slow or something.

.. code:: yaml

   groups:
   - name: aleksis
     rules:
     - alert: HighRequestLatency
       expr: histogram_quantile(0.999, sum(rate(django_http_requests_latency_seconds_by_view_method_bucket{instance="YOUR-INSTANCE",view!~"prometheus-django-metrics|healthcheck"}[15m])) by (job, le)) < 30
       for: 15m
       labels:
         severity: page
       annotations:
         summary: High request latency for 15 minutes

Grafana dashboard
~~~~~~~~~~~~~~~~~

There is a Grafana dashboard available to visualise the metrics.

The dashboard is available at
https://grafana.com/grafana/dashboards/9528.
