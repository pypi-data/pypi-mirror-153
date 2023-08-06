# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['connect', 'connect.eaas', 'connect.eaas.managers']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.11.1,<2.0.0',
 'connect-openapi-client>=25.3',
 'logzio-python-handler>=3.0.0,<4.0.0',
 'uvloop>=0.16.0,<0.17.0',
 'websockets>=10.0.0,<11.0.0']

entry_points = \
{'console_scripts': ['cextrun = connect.eaas.main:main']}

setup_kwargs = {
    'name': 'connect-extension-runner',
    'version': '25.1',
    'description': 'CloudBlue Connect EaaS Extension Runner',
    'long_description': '# CloudBlue Connect EaaS Extension Runner\n\n\n![pyversions](https://img.shields.io/pypi/pyversions/connect-extension-runner.svg) [![PyPi Status](https://img.shields.io/pypi/v/connect-extension-runner.svg)](https://pypi.org/project/connect-extension-runner/) [![Build Connect Reports Core](https://github.com/cloudblue/connect-extension-runner/actions/workflows/build.yml/badge.svg)](https://github.com/cloudblue/connect-extension-runner/actions/workflows/build.yml) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=connect-extension-runner&metric=alert_status)](https://sonarcloud.io/dashboard?id=connect-extension-runner) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=connect-extension-runner&metric=coverage)](https://sonarcloud.io/dashboard?id=connect-extension-runner) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=connect-extension-runner&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=connect-extension-runner)![Docker Image Version (latest semver)](https://img.shields.io/docker/v/cloudblueconnect/connect-extension-runner?label=docker%20version&sort=semver)![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/cloudblueconnect/connect-extension-runner?label=docker%20image%20size&sort=semver)![Docker Pulls](https://img.shields.io/docker/pulls/cloudblueconnect/connect-extension-runner)\n',
    'author': 'CloudBlue LLC',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://connect.cloudblue.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
