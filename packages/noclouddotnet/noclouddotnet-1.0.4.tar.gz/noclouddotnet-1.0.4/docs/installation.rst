Installation
============

A production setup should involve an Apache/mod_wsgi installation and a RDBMS
backend.  The noclouddotnet server itself is deployed as a wheel and should be
installed onto the host along with apache and mod_wsgi.

An example Apache configuration:

.. literalinclude:: ../config/apache.conf


The noclouddotnet application uses `Dynaconf <http://dynaconf.com>`_ for
configuration: thereare many ways to set/override variables.  An example
config is:

.. literalinclude:: ../config/settings.yaml


In order to create a/the RDBMS as per your configuration; you may need to do
something along the lines of the following:

.. code-block::
   :caption: database setup

    export FLASK_APP=noclouddotnet.app
    export FLASK_ENV=production
    export NOCLOUD_DOT_NET_SETTINGS=<path to settings.yaml>
    flask createdb
