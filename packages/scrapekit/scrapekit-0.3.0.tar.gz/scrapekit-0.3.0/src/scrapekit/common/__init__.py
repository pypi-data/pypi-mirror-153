""" Common modules

Credit for user-agent.json goes to: https://github.com/intoli/user-agents/
"""
import json
import logging
import random
from os import path


logger = logging.getLogger('scrapekit-common')
resources_dir = path.join(path.dirname(__file__), 'user-agents')


def get_user_agent(
        os:         str = 'Mac OS X',
        browser:    any = None,
        failsafe:   bool = True
) -> str:
    """ scrapekit.common.get_user_agent

    Get a User-Agent string. Defaults to a random user agent string.

    Use the os keyword argument to specify the host OS.

    Use the browser keyword argument to specify the browser.

    The failsafe argument will return a random user agent if a matching
    OS/browser combination cannot be found in the user agent library.

    Arguments:
        os:             Host OS string
                        Default: None

        browser:        Chosen browser
                        Default: None

        failsafe:       Return a user agent if the OS/browser pair cannot
                        be found in the user agent library
                        Default: True

    Returns:
        user_agent:     Randomly chosen user agent string
    """
    failsafe_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64' \
                     ' Safari/537.36'

    # Load user agent library
    try:
        with open(f'{resources_dir}/user-agents.json', 'r') as file:
            profiles = json.load(file)
            user_agents = [profile['userAgent'] for profile in profiles]
    except OSError as error:
        logger.warning('Could not read user-agents.json: %s', error)
        logger.warning('Current __file__: %s', __file__)
        if failsafe:
            return failsafe_agent
        else:
            return ''

    # OS filtering
    if os is not None:
        user_agents = [
            user_agent for user_agent in user_agents if os in user_agent
        ]

    # Browser filtering
    if browser is not None:
        user_agents = [
            user_agent for user_agent in user_agents if browser in user_agent
        ]

    if len(user_agents) == 0:
        if failsafe:
            return failsafe_agent
        else:
            return ''
    elif len(user_agents) == 1:
        return user_agents[0]
    else:
        return random.choice(user_agents)


__all__ = [
    get_user_agent
]