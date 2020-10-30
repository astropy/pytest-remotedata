# Licensed under a 3-clause BSD style license - see LICENSE.rst
# this test doesn't actually use any online data, it should just be skipped
# by run_tests because it has the remote_data decorator.

from contextlib import closing
from urllib.error import URLError
from urllib.request import urlopen

import pytest

ASTROPY_DATA_URL = "http://data.astropy.org/"
GITHUB_DATA_URL = "http://astropy.github.io/"
EXTERNAL_URL = "http://www.google.com"
TIMEOUT = 10


def download_file(remote_url):
    with closing(urlopen(remote_url, timeout=TIMEOUT)) as remote:
        remote.read()


@pytest.mark.remote_data
def test_skip_remote_data(pytestconfig):

    # astropy.test() has remote_data=none or remote_data=astropy but we still
    # got here somehow, so fail with a helpful message

    if pytestconfig.getoption('remote_data') == 'none':
        pytest.fail('@remote_data was not skipped with remote_data=none')
    elif pytestconfig.getoption('remote_data') == 'astropy':
        pytest.fail('@remote_data was not skipped with remote_data=astropy')
    elif pytestconfig.getoption('remote_data') == 'github':
        pytest.fail('@remote_data was not skipped with remote_data=github')

    # Test Astropy URL
    download_file(ASTROPY_DATA_URL + 'galactic_center/gc_2mass_k.fits')

    # Test GitHub URL
    download_file(GITHUB_DATA_URL)

    # Test unrelated URL
    download_file(EXTERNAL_URL)


@pytest.mark.remote_data(source='astropy')
def test_skip_remote_data_astropy(pytestconfig):

    # astropy.test() has remote_data=none but we still got here somehow,
    # so fail with a helpful message

    if pytestconfig.getoption('remote_data') in ('none', 'github'):
        pytest.fail('@remote_data was not skipped with remote_data=none'
                    'or remote_data=github')

    # Test Astropy URL
    download_file(ASTROPY_DATA_URL + 'galactic_center/gc_2mass_k.fits')

    # Test non-Astropy URL
    if pytestconfig.getoption('remote_data') == 'astropy':
        with pytest.raises(Exception) as exc:
            download_file(EXTERNAL_URL)
        assert "An attempt was made to connect to the internet" in str(exc.value)  # noqa
    else:  # remote_data=any
        download_file(EXTERNAL_URL)


@pytest.mark.remote_data(source='github')
def test_skip_remote_data_github(pytestconfig):
    if pytestconfig.getoption('remote_data') == 'none':
        pytest.fail('@remote_data was not skipped with remote_data=none')

    # Test GitHub URL
    download_file(GITHUB_DATA_URL)

    # Test non-GitHub URL
    if pytestconfig.getoption('remote_data') == 'github':
        with pytest.raises(Exception) as exc:
            download_file(ASTROPY_DATA_URL)
        assert "An attempt was made to connect to the internet" in str(exc.value)
    else:  # remote_data=any or remote_data=astropy
        download_file(ASTROPY_DATA_URL)


@pytest.mark.internet_off
def test_internet_off_decorator(pytestconfig):
    # This test should only run when internet access has been disabled
    if pytestconfig.getoption('remote_data') != 'none':
        pytest.fail('@internet_off test ran when remote_data!=none')


def test_block_internet_connection(pytestconfig):
    if pytestconfig.getoption('remote_data') == 'none':
        with pytest.raises(URLError):
            download_file(EXTERNAL_URL)
    elif pytestconfig.getoption('remote_data') == 'astropy':
        with pytest.raises(URLError):
            download_file(EXTERNAL_URL)
    elif pytestconfig.getoption('remote_data') == 'github':
        with pytest.raises(URLError):
            download_file(EXTERNAL_URL)
    else:
        download_file(EXTERNAL_URL)


@pytest.mark.internet_off
def test_block_internet_connection_internet_off():
    with pytest.raises(URLError):
        download_file(EXTERNAL_URL)
