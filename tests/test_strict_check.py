# Licensed under a 3-clause BSD style license - see LICENSE.rst

from typing import assert_never, Literal, TypeAlias, TypedDict

import pytest

PYFILE_CONTENTS = """
    import pytest
    from urllib.request import urlopen

    def test_config_setting(pytestconfig):
        assert pytestconfig.getini({option_name!r}) == {expected_value}

    {decorator}
    def test_internet_access():
        urlopen('http://astropy.org')
    """

ConfigTarget: TypeAlias = Literal['pyproject.toml', 'pyproject.toml-legacy', 'setup.cfg']

def _write_config_file(
    testdir,
    entry: str,
    *,
    target: ConfigTarget,
) -> None:
    match target:
        case 'pyproject.toml':
            section = '[tool.pytest]'
        case 'pyproject.toml-legacy':
            section = '[tool.pytest.ini_options]'
        case 'setup.cfg':
            section = '[tool:pytest]'
        case _ as unreachable:
            assert_never(unreachable)

    filename, _, _ = target.partition('-')
    config = testdir.tmpdir.join(filename)
    config.write(f"{section}\n{entry}")

    # Just a sanity check to make sure we actually write the config file
    assert config.isfile()


def test_local_config(pytestconfig):
    assert pytestconfig.getini('remote_data_strict') is True
    if pytest.version_tuple >= (9, 0, 0):
        assert pytestconfig.getini('strict_remote_data') is True


def test_default_behavior(testdir):
    testdir.makepyfile(
        PYFILE_CONTENTS.format(
            option_name='remote_data_strict',
            expected_value=None if pytest.version_tuple >= (8,) else [],
            decorator='',
        )
    )

    result = testdir.runpytest_subprocess()
    result.assert_outcomes(passed=2)


option_names = [
    'remote_data_strict',
    pytest.param(
        'strict_remote_data',
        marks=pytest.mark.skipif(
            pytest.version_tuple < (9,),
            reason="alias is only supported for pytest 9 and newer",
        )
    ),
    pytest.param(
        'strict',
        marks=pytest.mark.skipif(
            pytest.version_tuple < (9,),
            reason="strict mode is only supported in pytest 9 and newer",
        )
    ),
]
targets = [
    'setup.cfg',
    'pyproject.toml-legacy',
    pytest.param(
        'pyproject.toml',
        marks=pytest.mark.skipif(
            pytest.version_tuple < (9,),
            reason="native toml config is only supported in pytest 9 and newer",
        ),
    ),
]

@pytest.mark.parametrize('option_name', option_names)
@pytest.mark.parametrize('target', targets)
def test_strict_behavior(testdir, option_name: str, target: ConfigTarget):
    _write_config_file(testdir, f"{option_name} = true", target=target)

    testdir.makepyfile(
        PYFILE_CONTENTS.format(
            option_name=option_name,
            expected_value=True,
            decorator='',
        )
    )

    result = testdir.runpytest_subprocess()
    result.assert_outcomes(passed=1, failed=1)


class Outcomes(TypedDict, total=False):
    passed: int
    failed: int
    skipped: int



@pytest.mark.parametrize(
    "source, expected_outcomes",
   [
       ('none', {"passed": 1, "skipped": 1}),
       ('any', {"passed": 2}),
   ],
)
@pytest.mark.parametrize('option_name', option_names)
@pytest.mark.parametrize('target', targets)
def test_strict_with_decorator(
    testdir,
    source: Literal['any', 'none'],
    expected_outcomes: Outcomes,
    option_name: str,
    target: ConfigTarget,
) -> None:
    _write_config_file(testdir, f"{option_name} = true", target=target)

    testdir.makepyfile(
        PYFILE_CONTENTS.format(
            option_name=option_name,
            expected_value=True,
            decorator='@pytest.mark.remote_data',
        )
    )

    clarg = '--remote-data=' + source
    result = testdir.runpytest_subprocess(clarg)
    result.assert_outcomes(**expected_outcomes)
