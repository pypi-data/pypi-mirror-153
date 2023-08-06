# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecr_scan_reporter']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.22,<2.0', 'compose-x-common>=1.0,<2.0', 'pytz>=2022.1,<2023.0']

entry_points = \
{'console_scripts': ['ecr_scan_reporter = ecr_scan_reporter.cli:main']}

setup_kwargs = {
    'name': 'ecr-scan-reporter',
    'version': '0.4.7',
    'description': 'Stay on top of your docker images security vulnerabilities in AWS ECR',
    'long_description': '=================\nECR Scan Reporter\n=================\n\n\n.. image:: https://img.shields.io/pypi/v/ecr_scan_reporter.svg\n        :target: https://pypi.python.org/pypi/ecr_scan_reporter\n\n\n------------------------------------------------------------------------------------\nServerless Application to monitor ECR Repositories and capture scan results\n------------------------------------------------------------------------------------\n\nWorkflow\n==========\n\n.. image:: https://ecr-scan-reporter.compose-x.io/_images/EcrScanReporterWorkflow.jpg\n\n\nFull documentation https://ecr-scan-reporter.compose-x.io.\n\nInstall from `AWS Serveless Applications Repository`_\n\nCredits\n-------\n\nThis package was created with Cookiecutter_.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _AWS Serveless Applications Repository: https://serverlessrepo.aws.amazon.com/applications/eu-west-1/518078317392/ecr-scan-reporter\n',
    'author': 'John Preston',
    'author_email': 'john@compose-x.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
