=================
pytest-remotedata
=================

.. image:: https://github.com/astropy/pytest-remotedata/workflows/Run%20unit%20tests/badge.svg
    :target: https://github.com/astropy/pytest-remotedata/actions
    :alt: CI Status

This package provides a plugin for the `pytest`_ framework that allows
developers to control unit tests that require access to data from the internet.
It was originally part of the `astropy`_ core package, but has been moved to a
separate package in order to be of more general use.

.. _pytest: https://pytest.org/en/latest/
.. _astropy: https://astropy.org/


Motivation
----------

Many software packages provide features that require access to data from the
internet. These features need to be tested, but unit tests that access the
internet can dominate the overall runtime of a test suite.

The ``pytest-remotedata`` plugin allows developers to indicate which unit tests
require access to the internet, and to control when and whether such tests
should execute as part of any given run of the test suite.

Installation
------------

The ``pytest-remotedata`` plugin can be installed using ``pip``::

    $ pip install pytest-remotedata

It is also possible to install the latest development version from the source
repository::

    $ git clone https://github.com/astropy/pytest-remotedata
    $ cd pytest-remotedata
    $ pip install .

In either case, the plugin will automatically be registered for use with
``pytest``.

Usage
-----

Installing this plugin makes two decorators available for use with ``pytest``:

* ``remote_data`` for marking tests that require data from the internet
* ``internet_off`` for marking tests that should run only when internet access
  is disabled

These decorators can be used to mark test functions, methods, and classes using
``@pytest.mark``. For example, consider the following test function that
requires access to data from the internet:

.. code-block:: python

    import pytest
    from urllib.request import urlopen

    @pytest.mark.remote_data
    def test_remote_data():
        urlopen('https://astropy.org')

Marking the ``test_remote_data`` function with ``@pytest.mark.remote_data``
indicates to ``pytest`` that this test should be run only when access to remote
data sources is explicitly requested.

When this plugin is installed, the ``--remote-data`` command line option is
added to the ``pytest`` command line interface.

The default behavior is to skip tests that are marked with ``remote_data``.
If the ``--remote-data`` option is not provided to the ``pytest`` command, or
if ``--remote-data=none`` is provided, all tests that are marked with
``remote_data`` will be skipped. All tests that are marked with
``internet_off`` will be executed.

Sometimes it is useful to check that certain tests do not unexpectedly access
the internet. Strict remote data access checking can be enabled by setting
``remote_data_strict = true`` in the tested package's ``setup.cfg`` file. If
this option is enabled, any test that attempts to access the network but is not
marked with ``@pytest.mark.remote_data`` will fail.


Providing either the ``--remote-data`` option, or ``--remote-data=any`` to the
``pytest`` command line interface will cause all tests that are marked with
``remote-data`` to execute. Any tests that are marked with ``internet_off``
will be skipped.

Running the tests with ``--remote-data=astropy`` will cause only tests that
receive remote data from Astropy data sources to be run. Tests with any other
data sources will be skipped. This is indicated in the test code by marking
test functions with ``@pytest.mark.remote_data(source='astropy')``.

In the future, we intend to support a configurable way to indicate specific
remote data sources in addition to ``astropy``.

Development Status
------------------

Questions, bug reports, and feature requests can be submitted on `github`_.

.. _github: https://github.com/astropy/pytest-remotedata

License
-------
This plugin is licensed under a 3-clause BSD style license - see the
``LICENSE.rst`` file.
