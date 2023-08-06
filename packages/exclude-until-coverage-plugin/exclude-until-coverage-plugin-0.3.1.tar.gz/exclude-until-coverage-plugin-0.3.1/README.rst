
Exclude Until Coverage Plugin
=============================

.. start-badges

|license|

.. |license| image:: https://img.shields.io/pypi/l/django_coverage_plugin.svg
    :target: https://pypi.python.org/pypi/exclude_until_coverage_plugin
    :alt: Apache 2.0 License

.. end-badges

A `coverage.py`_ plugin that excludes lines until a marker is found.

The plugin is pip installable::

    $ pip install exclude-until-coverage-plugin

To run it, add this setting to your ``.coveragerc`` file::

    [run]
    plugins =
        exclude_until_coverage_plugin

Then run your tests under `coverage.py`_.
This will use the default marker ``# = exclude above lines =`` and exclude all lines above the line this text appears on.
Use the plugin options to change the marker.
To change the marker, add this configuration value to your ``.coveragerc`` file::

    [exclude_until_coverage_plugin]
    marker=# my marker

.. _coverage.py: http://nedbatchelder.com/code/coverage
