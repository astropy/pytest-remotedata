# Licensed under a 3-clause BSD style license - see LICENSE.rst
import socket
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import TCPServer
from threading import Thread
from unittest import mock
from urllib.request import urlopen

import pytest
from pytest_remotedata.disable_internet import no_internet, socket_original


def test_outgoing_fails():
    with pytest.raises(IOError):
        with no_internet():
            urlopen('http://www.python.org')


def test_outgoing_fails_with_patched_socket():
    # Regression test for the blocker raising TypeError when a test has
    # replaced socket.socket with something that is not a type
    sock = socket_original(socket.AF_INET, socket.SOCK_STREAM)
    with sock, no_internet(), mock.patch('socket.socket'):
        with pytest.raises(OSError, match='connect to the internet'):
            sock.connect(('www.python.org', 80))


class StoppableHTTPServer(HTTPServer):
    def __init__(self, *args):
        super().__init__(*args)
        self.stop = False

    def server_bind(self):
        # Bypass HTTPServer.server_bind, which calls socket.getfqdn() and
        # can take tens of seconds on some systems (e.g. macOS CI runners)
        TCPServer.server_bind(self)
        self.server_name, self.server_port = self.server_address[:2]

    def handle_request(self):
        self.stop = True
        super().handle_request()

    def serve_forever(self):
        """
        Serve until stop set, which will happen if any request is handled
        """
        while not self.stop:
            self.handle_request()


@pytest.mark.parametrize(('localhost'),
                         ('localhost', '127.0.0.1', socket.gethostname()))
def test_localconnect_succeeds(localhost):
    """
    Ensure that connections to localhost are allowed, since these are genuinely
    not remotedata.
    """

    with no_internet():
        # port "0" means find open port
        # see http://stackoverflow.com/questions/1365265/on-localhost-how-to-pick-a-free-port-number
        httpd = StoppableHTTPServer(('localhost', 0), SimpleHTTPRequestHandler)

        port = httpd.socket.getsockname()[1]

        server = Thread(target=httpd.serve_forever)
        server.daemon = True

        server.start()
        time.sleep(0.1)

        urlopen(f'http://{localhost:s}:{port:d}').close()
        httpd.server_close()


# Used for the below test--inline functions aren't pickleable
# by multiprocessing?
def _square(x):
    return x ** 2


@pytest.mark.skipif('sys.platform == "win32" or sys.platform.startswith("gnu0")')
def test_multiprocessing_forkserver():
    """
    Test that using multiprocessing with forkserver works.  Perhaps
    a simpler more direct test would be to just open some local
    sockets and pass something through them.

    Regression test for https://github.com/astropy/astropy/pull/3713
    """

    import multiprocessing
    ctx = multiprocessing.get_context('forkserver')
    pool = ctx.Pool(1)
    result = pool.map(_square, [1, 2, 3, 4, 5])
    pool.close()
    pool.join()
    assert result == [1, 4, 9, 16, 25]
