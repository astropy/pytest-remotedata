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
