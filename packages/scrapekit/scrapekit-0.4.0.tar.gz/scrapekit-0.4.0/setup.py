# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scrapekit', 'scrapekit.common', 'scrapekit.ipburger']

package_data = \
{'': ['*'], 'scrapekit.common': ['user-agents/*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'scrapekit',
    'version': '0.4.0',
    'description': 'Modular scraping convenience framework written in Python.',
    'long_description': '# scrapekit\nModular scraping convenience framework.\n\n**Convenience Methods**:\n\n- `scrapekit.common.get_user_agent(os, browser)`: Returns a random User-Agent string.\n  - Can filter by OS and browser\n\n**Proxy Provider Module List**:\n\n- [IP Burger](https://secure.ipburger.com/aff.php?aff=1479&page=residential-order)\n\n## Installation\n```shell\npip install scrapekit\n```\n\n## Usage Examples\n\n**Simple proxified session**\n\n```python\nimport scrapekit\n\nsession = scrapekit.ipburger.make_session(\'MyIPBurgerUsername")\n\nres = session.get(\'https://icanhazip.com\')\nprint(res.status_code, res.text)\n# 200 89.46.62.37\n```\n\n**Proxified session with random Windows Firefox User-Agent**:\n\n```python\nimport scrapekit\n\nuser_agent = scrapekit.common.get_user_agent(os=\'Windows\', browser=\'Firefox\')\nsession = scrapekit.ipburger.make_session(\n    \'MyIPBurgerUsername\',\n    headers={\'User-Agent\': user_agent}\n)\n```',
    'author': 'C. Weber',
    'author_email': 'c@omniviant.com',
    'maintainer': 'C. Weber',
    'maintainer_email': 'c@omniviant.com',
    'url': 'https://bitbucket.org/chad-og/scrapekit/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
