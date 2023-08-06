
|CI|

Site Configuration Client
=========================

REST API client for the Site Configuration service.

Compatibility
=============

This package tested with both Python 3.9 and Python 3.5.

It has few required and optional dependencies:

-  **requests:** Required. Explicitly specified in ``setup.py``
-  **django:** Optional. Tested to work with both Django 3 and
   Django 2.
-  **google-cloud-storage:** Optional. Tested with version 1.x.

For the exact versions please refer to both ``setup.py`` and the
``requirements`` directory.


Installation
============

Install the ``site-configuration-client`` dependency from PyPi either via ``server-vars.yml`` or other build processes such as Docker.

Add the following settings to ``server-vars.yml`` (or ``lms.yml`` depending on your deployment configuration).


.. code:: yaml

    SITE_CONFIG_BASE_URL: "https://siteconfig:14000/"
    SITE_CONFIG_API_TOKEN: "api token goes here"
    SITE_CONFIG_ENVIRONMENT: "development"


.. |CI| image:: https://github.com/appsembler/site-configuration-client/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/appsembler/site-configuration-client/actions/workflows/tests.yml
