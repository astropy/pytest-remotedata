# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This plugin provides command-line options for controlling whether and how tests
make use of online data.
"""
import pytest

from .disable_internet import turn_off_internet, turn_on_internet


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup('pytest-remote-data')

    # The following means that if --remote-data is not specified, the default
    # is 'none', but if it is specified without arguments (--remote-data), it
    # defaults to '--remote-data=any'.
    group.addoption(
        "--remote-data", nargs="?", const='any', default='none',
        dest="remote_data", help="run tests with online data",
        choices=['astropy', 'any', 'github', 'none'])

    if pytest.version_tuple >= (9, 0, 0):
        # 'strict_'-prefixed option names are prefered over their
        # historical '_strict'-suffixed counterparts since pytest 9,
        # so this name should really be the default instead of an alias,
        # but defining aliases itself requires pytest 9, so to preserve
        # backward compatibility, this relationship is reverted and the new
        # prefered name is only available for pytest 9 and newer
        version_spec_kwargs = {'aliases': ("strict_remote_data",)}
    else:
        version_spec_kwargs = {}

    parser.addini(
        "remote_data_strict",
        type="bool",
        # None => fallback to `strict` in pytest 9
        # rely on the falsiness of None otherwise
        default=None,
        help=(
            "If 'True', tests will fail if they attempt to access the internet "
            "but are not explicitly marked with 'remote_data'"
        ),
        **version_spec_kwargs,
    )

    if pytest.version_tuple >= (9, 0, 0):
        from _pytest.config.argparsing import OverrideIniAction

        group.addoption(
            "--strict-remote-data",
            action=OverrideIniAction,
            ini_option="strict_remote_data",
            ini_value="true",
            help="Enables the strict_remote_data option",
        )


def pytest_configure(config):
    config.getini('markers').append(
        'remote_data: Apply to tests that require data from remote servers')
    config.getini('markers').append(
        'internet_off: Apply to tests that should only run when '
        'network access is deactivated')

    strict_check = config.getini('remote_data_strict')
    if strict_check is None and pytest.version_tuple >= (9, 0, 0):
        strict_check = config.getini('strict')

    if not strict_check:
        return

    # Monkeypatch to deny access to remote resources unless explicitly told
    # otherwise
    match remote_data := config.getoption('remote_data'):
        case 'any':
            pass
        case 'github' | 'astropy' | 'none':
            turn_off_internet(
                verbose=config.option.verbose,
                allow_github_data=(remote_data == 'github'),
                allow_astropy_data=(remote_data == 'astropy'),
            )
        case _ as _unreachable:
            raise AssertionError(f'Unexpected value for {remote_data=!r}')


def pytest_unconfigure():
    """
    Cleanup post-testing
    """
    # restore internet connectivity (only lost if remote_data=False and
    # turn_off_internet previously called)
    # this is harmless / does nothing if socket connections were never disabled
    turn_on_internet()


def pytest_runtest_setup(item):

    remote_data = item.get_closest_marker('remote_data')
    internet_off = item.get_closest_marker('internet_off')

    remote_data_config = item.config.getvalue("remote_data")

    if remote_data is not None and internet_off is not None:
        raise ValueError("remote_data and internet_off are not compatible")

    if remote_data is not None:
        if len(remote_data.args) > 0:
            source = remote_data.args[0]
        else:
            source = remote_data.kwargs.get('source', 'any')

        if source not in ('astropy', 'any', 'github'):
            raise ValueError("source should be 'astropy', 'any', or 'github'")

        if remote_data_config == 'none':
            pytest.skip("need --remote-data option to run")
        elif remote_data_config == 'github':
            if source in ('any', 'astropy'):
                pytest.skip("need --remote-data or "
                            "--remote-data=astropy option to run")
        elif remote_data_config == 'astropy':
            # When --remote-data=astropy is given, skip tests simply
            # marked as --remote-data
            if source == 'any':
                pytest.skip("need --remote-data option to run")

    if internet_off is not None:
        if remote_data_config != 'none':
            pytest.skip("run this test only when network access is disabled")
