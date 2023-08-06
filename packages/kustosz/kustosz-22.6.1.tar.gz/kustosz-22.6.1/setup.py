# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kustosz',
 'kustosz.cli',
 'kustosz.fetchers',
 'kustosz.forms',
 'kustosz.management',
 'kustosz.management.commands',
 'kustosz.migrations',
 'kustosz.tasks',
 'kustosz.third_party',
 'kustosz.third_party.taggit_serializer',
 'kustosz.utils']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.13,<4.0.0',
 'Unalix>=0.9,<0.10',
 'celery>=5.2.6,<6.0.0',
 'django-celery-beat>=2.2.1,<3.0.0',
 'django-celery-results>=2.3.1,<3.0.0',
 'django-cors-headers>=3.12.0,<4.0.0',
 'django-extensions>=3.1.5,<4.0.0',
 'django-filter>=21.1,<22.0',
 'django-taggit-serializer>=0.1.7,<0.2.0',
 'django-taggit>=2.1.0,<3.0.0',
 'djangorestframework>=3.13.1,<4.0.0',
 'dynaconf[yaml]>=3.1.8,<4.0.0',
 'hyperlink>=21.0.0,<22.0.0',
 'listparser>=0.18,<0.19',
 'readability-lxml>=0.8.1,<0.9.0',
 'reader>=2.12,<3.0',
 'requests-cache>=0.9.4,<0.10.0']

extras_require = \
{'container': ['gunicorn>=20.1.0,<21.0.0',
               'psycopg2>=2.9.3,<3.0.0',
               'redis>=4.2.2,<5.0.0',
               'whitenoise>=6.0.0,<7.0.0'],
 'heroku': ['dj-database-url>=0.5.0,<0.6.0',
            'gunicorn>=20.1.0,<21.0.0',
            'supervisor>=4.2.4,<5.0.0',
            'psycopg2-binary>=2.9.3,<3.0.0',
            'redis>=4.2.2,<5.0.0',
            'whitenoise>=6.0.0,<7.0.0'],
 'installer': ['gunicorn>=20.1.0,<21.0.0', 'redis>=4.2.2,<5.0.0']}

entry_points = \
{'console_scripts': ['kustosz-manager = kustosz.cli.manage:main']}

setup_kwargs = {
    'name': 'kustosz',
    'version': '22.6.1',
    'description': 'Focus on the worthwhile content with Kustosz, open source self-hosted web application. This package contains backend server.',
    'long_description': "[![Kustosz](./kustosz_logo.svg)](https://www.kustosz.org)\n\n![GitHub](https://img.shields.io/github/license/KustoszApp/server?color=green) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kustosz?color=green) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/KustoszApp/server/CI?label=CI) ![GitHub issues](https://img.shields.io/github/issues/KustoszApp/server?color=green) ![GitHub pull requests](https://img.shields.io/github/issues-pr/KustoszApp/server) ![GitHub Repo stars](https://img.shields.io/github/stars/KustoszApp/server?color=green) ![GitHub Release Date](https://img.shields.io/github/release-date/KustoszApp/server) ![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/KustoszApp/server/latest?color=green) ![GitHub last commit](https://img.shields.io/github/last-commit/KustoszApp/server)\n\n# Kustosz - backend server repository\n\nFocus on the worthwhile content with Kustosz, open source self-hosted web application.\n\nThis repository contains backend server.\n\n## Installation\n\nSee [Kustosz installation documentation](https://docs.kustosz.org/en/stable/installation.html) for instructions on how to deploy or try Kustosz.\n\nSee [backend development documentation](https://docs.kustosz.org/en/stable/development/backend.html) for instructions on how to build Kustosz backend from source and run development version of code.\n\n## Contributing\n\nAll contributions are welcome!\n\nIf you have found a problem or want to ask a question, feel free to [submit an issue](https://github.com/KustoszApp/server/issues). There's no template to follow. Usually it's good idea to describe what did you do, what did you expect to happen and what happened instead.\n\nIf you want to contribute code, just fork the repository and [submit a pull request](https://github.com/KustoszApp/server/pulls). Instructions on setting up local development environment can be found at [docs.kustosz.org](https://docs.kustosz.org/en/stable/development/backend.html).\n\n## License\n\nKustosz is distributed under terms of [European Union Public Licence](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)\n",
    'author': 'Mirek Długosz',
    'author_email': 'mirek@mirekdlugosz.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.kustosz.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
