Running tests and reports
=========================

Running default test suite
--------------------------

The test suite can be run using the `tox` tool::

  tox

Enabling Selenium browser tests
-------------------------------

The test suite contains tests that use Selenium to do browser based tests.
They need to be enabled when running the test suite, which can be done by
setting certain environment variables:

+------------------------+------------------------------------------------------+------------------------------+
| Variable               | Meaning                                              | Example                      |
+========================+======================================================+==============================+
| TEST_SELENIUM_BROWSERS | List of webdrivers to test against, comma-separated. | chrome,firefox               |
+------------------------+------------------------------------------------------+------------------------------+
| TEST_SELENIUM_HUB      | Address of Selenium hub if using remote grid         | http://127.0.0.1:4444/wd/hub |
+------------------------+------------------------------------------------------+------------------------------+
| TEST_HOST              | Hostname reachable from Selenium for live server     | 172.17.0.1                   |
+------------------------+------------------------------------------------------+------------------------------+
| TEST_SCREENSHOT_PATH   | Path to directory to create screenshots in           | ./screenshots                |
+------------------------+------------------------------------------------------+------------------------------+

Selenium tests are enabled if `TEST_SELENIUM_BROWSERS` is non-empty.

To set variables, use env to wrap the tox ommand::

  TEST_SELENIUM_BROWSERS=chrome,firefox tox


Using a Selenium hub on local Docker host
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One way to setup Selenium is to use the official images on the local
machine.

First, get Selenium Hub and one or more browser nodes up and running::

  docker run -d -p 4444:4444 --name selenium-hub selenium/hub
  docker run -d --link selenium-hub:hub selenium/node-chrome
  docker run -d --link selenium-hub:hub selenium/node-firefox

After that, you can run the test suite, setting the needed variables to use
Docker Hub::

  TEST_SELENIUM_BROWSERS=chrome,firefox \
  TEST_SELENIUM_HUB=http://127.0.0.1:4444/wd/hub \
  TEST_HOST=172.17.0.1 \
  tox

The `TEST_HOST` variable is set to the Docker host's IP address, where the
Selenium nodes can access Django's live server.  Django automatically
configures the live server to be reachable if a Selenium hub is used.


Taking screenshots
~~~~~~~~~~~~~~~~~~

The browser test suites automatically take screenshots at certain steps if
enabled in the test run.  This can be used to visually verify that views
look like they should or for documentation purposes.

To enable screenshots, add the `TEST_SCREENSHOT_PATH` environment variable
when running the tests.

If runnin multiple browsers, screenshots are placed in separate directories
per browser.
