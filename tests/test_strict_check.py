# Licensed under a 3-clause BSD style license - see LICENSE.rst

import os
import pytest

PYFILE_CONTENTS = """
    import pytest
    from urllib.request import urlopen

    def test_config_setting(pytestconfig):
        assert pytestconfig.getini('remote_data_strict') == {}

    {}
    def test_internet_access():
        urlopen('http://astropy.org')
    """

def _write_config_file(testdir, entry):
    config = testdir.tmpdir.join('setup.cfg')
    config.write("""
[tool:pytest]
{}
        """.format(entry))

    # Just a sanity check to make sure we actually write the config file
    assert os.path.exists(str(testdir.tmpdir.join('setup.cfg')))


def test_local_config(pytestconfig):
    assert pytestconfig.getini('remote_data_strict') == True


def test_default_behavior(testdir):
    _write_config_file(testdir, '')

    testdir.makepyfile(PYFILE_CONTENTS.format('False', ''))

    result = testdir.runpytest_subprocess()
    result.assert_outcomes(passed=2)


def test_strict_behavior(testdir):
    _write_config_file(testdir, 'remote_data_strict = true')

    testdir.makepyfile(PYFILE_CONTENTS.format('True', ''))

    result = testdir.runpytest_subprocess()
    result.assert_outcomes(passed=1, failed=1)


@pytest.mark.parametrize('source', ['none', 'any'])
def test_strict_with_decorator(testdir, source):
    _write_config_file(testdir, 'remote_data_strict = true')

    decorator = '@pytest.mark.remote_data'
    testdir.makepyfile(PYFILE_CONTENTS.format('True', decorator))

    clarg = '--remote-data=' + source
    result = testdir.runpytest_subprocess(clarg)

    if source == 'none':
        outcomes = dict(passed=1, skipped=1)
    else:
        outcomes = dict(passed=2)
    result.assert_outcomes(**outcomes)
