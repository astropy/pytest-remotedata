0.4.3 (2026-10-27)
==================

- The ``--remote-data`` option now sets its ``dest`` explicitly so that
  it can share it with a short option defined by another plugin (e.g.,
  ``-R`` in ``pytest-astropy``) with the development version of
  pytest. [#102]

- The socket blocker no longer calls ``socket.getfqdn()`` on every
  intercepted connection. This could take tens of seconds per call on
  some systems (e.g. macOS CI runners). Connections to the machine's own
  hostname or fully qualified domain name are now detected by checking
  whether the resolved address is local. The addresses of the allowed
  data hosts are also now only resolved once per process. [#106]

- Versions of Python <3.11 and pytest <7.2 are no longer supported. [#106]

- The package is now built with ``hatchling`` and all packaging metadata
  lives in ``pyproject.toml``. [#106]

- Fixed a ``TypeError`` in the socket blocker when ``socket.socket`` has
  been replaced (e.g. by a mock) in the test being run.

0.4.2 (2026-08-03)
==================

- Versions of Python <3.9 are no longer supported. [#81, #93]

0.4.1 (2023-09-25)
==================

- Reverting the short option of ``-R`` due to a clash with ``pytest-leaks``.
  The short option is added to ``pytest-astropy`` instead. [#70]

0.4.0 (2022-12-11)
==================

- ``-R`` is added as a short version for the command-line option
  ``--remote-data``. [#62]

- Versions of Python <3.7 are no longer supported. [#65]

0.3.3 (2021-12-21)
==================

- Various infrastructure and packaging updates. If you have trouble
  installing an older version, try upgrading to this one.

0.3.2 (2019-07-20)
==================

- Fixed compatibility with pytest 4.2 and later. [#38, #40]

0.3.1 (2018-10-23)
==================

- Fix warnings that occur with pytest 3.7 and later. [#34]

0.3.0 (2018-05-29)
==================

- Allow ``remote_data`` argument to be passed without ``source`` keyword. [#27]

- Add ``source='github'`` option. Also fix IP lookup error for
  ``source='astropy'`` option. [#28]

0.2.1 (2018-04-20)
==================

- Fix packaging error: tests are no longer included in package distribution.
  [#24]

0.2.0 (2017-11-10)
==================

- Do not accept invalid values passed to ``--remote-data`` argument. [#15]

- Update list of valid hosts URLs recognized as astropy data sources. [#13]

- Remove test dependency on astropy core. [#14]

- Allow strict remote data checking to be configurable. This introduces a
  dependency on ``pytest>=3.1``. [#18]

0.1 (2017-10-10)
================

- Alpha release.
