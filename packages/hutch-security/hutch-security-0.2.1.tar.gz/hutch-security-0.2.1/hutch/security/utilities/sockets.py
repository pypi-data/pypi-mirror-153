"""Provides socket related utility functions."""
import json
import socket

import requests
import urllib3

from hutch.security.utilities.constants import PROTOCOL_SCHEMES, WRONG_TRANSPORT
from hutch.security.utilities.exceptions import SocketException, UnknownSchemeException


def listening(host: str, port: int) -> bool:
    """Check whether a port responds to connection attempts, returning a boolean.

    :param host: The hostname or IP address of the host to attempt to connect to.
    :param port: The port to attempt to connect to on the host.

    :returns: True if the target responds, False if not.
    """
    # DNS Names may be passed, which will need to have their IPs looked up before trying
    # to connect. In these cases, there may be more than one IP, so we'll scan them all
    # and return if any one of them respond.
    addresses = set()

    try:
        addrinfo = socket.getaddrinfo(host, 0, proto=socket.IPPROTO_TCP)
    except socket.gaierror as err:
        return SocketException(f"Unable to lookup DNS records for host {host}: {err}")

    for ip in addrinfo:
        # sockaddr is the fifth element in the response from getaddrinfo. The address is
        # the first element of sockaddr.
        try:
            sockaddr = ip[4]
            addresses.add(sockaddr[0])
        except IndexError:
            continue

    for candidate in addresses:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((candidate, int(port)))

            return True
        except (ConnectionRefusedError, socket.timeout):
            pass

    # Default to no response.
    return False


def scheme(host: str, port: int) -> str:
    """Attempts to determine the protocol scheme for a given target.

    :param host: The hostname or IP address of the host to attempt to connect to.
    :param port: The port to attempt to connect to on the host.

    :returns: The identified protocol scheme for the target.
    """
    # Suppress warnings as we intentionally want to accept invalid certificates.
    urllib3.disable_warnings()

    # Ensure the target is actually listening, first.
    if not listening(host, port):
        raise SocketException(f"Socket on {host}:{port} is not listening.")

    for scheme in PROTOCOL_SCHEMES:
        uri = f"{scheme}://{host}:{port}"

        try:
            response = requests.get(
                uri,
                verify=False,  # noqa: S501
                allow_redirects=False,
                timeout=5,
            )
            response.raise_for_status()

            # Golang net/http and Tomcat try to be too helpful, so ignore these replies
            # as although we got a response the scheme is wrong.
            for warning in WRONG_TRANSPORT:
                if warning in response.content:
                    continue

            return scheme
        except requests.exceptions.RequestException:
            continue
        except json.decoder.JSONDecodeError:
            continue

    raise UnknownSchemeException(
        f"Socket on {host}:{port} is listening, but protocol scheme is unknown"
    )
