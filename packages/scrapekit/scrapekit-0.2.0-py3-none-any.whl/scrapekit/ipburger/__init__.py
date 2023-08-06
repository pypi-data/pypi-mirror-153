""" IP Burger Proxy Module """
import random

import requests


def make_session(
        username: str,
        port: str='',
        location: str='us',
        headers=None
) -> requests.Session:
    """ scrapekit.ipburger.make_session

    Creates a proxified requests.Session object.

    If using a sticky session, the port can be passed
    in the port argument.

    To choose a specific exit location, pass the IP Burger
    location string in the location argument.

    To specify additional request session headers, include
    them in the headers argument.

    Arguments:
        username:           IP Burger profile username

        port:               Port to use for sticky session.
                            Default: None

        location:           Location string
                            Default: 'us'

        headers:            Dictionary of HTTP headers to add to session.
                            Default: None

    Returns:
        sessions:           Proxified requests.Session object
    """
    if port == '':
        port = str(random.randint(10000, 10299))

    session = requests.Session()

    credentials = f'{username}:wifi;{location};;;;'
    url = f'http://{credentials}@resi3.ipb.cloud:{port}'
    session.proxies = {
        'http': {url},
        'https': {url},
    }

    if headers is not None:
        session.headers.update(headers)

    return session


__all__ = [
    make_session
]