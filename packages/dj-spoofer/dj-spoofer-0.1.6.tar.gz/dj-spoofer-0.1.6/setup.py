# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djspoofer',
 'djspoofer.management',
 'djspoofer.management.commands',
 'djspoofer.migrations',
 'djspoofer.remote',
 'djspoofer.remote.h2fingerprint',
 'djspoofer.remote.howsmyssl',
 'djspoofer.remote.incolumitas',
 'djspoofer.remote.intoli',
 'djspoofer.remote.ja3er',
 'djspoofer.remote.proxyrack',
 'djspoofer.remote.twocaptcha',
 'djspoofer.tests',
 'djspoofer.tests.djspoofer',
 'djspoofer.tests.h2_fingerprint',
 'djspoofer.tests.h2_fingerprint.resources',
 'djspoofer.tests.howsmyssl',
 'djspoofer.tests.howsmyssl.resources',
 'djspoofer.tests.incolumitas',
 'djspoofer.tests.incolumitas.resources',
 'djspoofer.tests.intoli',
 'djspoofer.tests.intoli.resources',
 'djspoofer.tests.ja3er',
 'djspoofer.tests.ja3er.resources',
 'djspoofer.tests.proxyrack',
 'djspoofer.tests.proxyrack.resources',
 'djspoofer.tests.twocaptcha',
 'djspoofer.tests.twocaptcha.resources']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.4,<4.0.0',
 'Faker>=8.12.1,<8.13.0',
 'coverage>=6.2,<7.0',
 'dj-starter>=0.1.11,<0.2.0',
 'django-environ>=0.8.1,<0.9.0',
 'django-import-export>=2.8.0,<3.0.0',
 'httpx[http2]>=0.22.0,<0.23.0',
 'psycopg2-binary>=2.9.2,<3.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'ua-parser>=0.10.0,<0.11.0',
 'urllib3>=1.26.9,<2.0.0',
 'wheel>=0.36.2,<0.37.0']

setup_kwargs = {
    'name': 'dj-spoofer',
    'version': '0.1.6',
    'description': 'Django + Web Scraping Made Easy',
    'long_description': None,
    'author': 'Adrian',
    'author_email': 'adrian@rydeas.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adrianmeraz/dj-spoofer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
