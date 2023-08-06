# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli',
 'cli.actions',
 'cli.ansible',
 'cli.ansible.connection',
 'cli.commands',
 'cli.constants',
 'cli.data',
 'cli.helpers',
 'cli.helpers.check',
 'cli.helpers.ec2',
 'cli.saml_clients',
 'cli.tests',
 'cli.tests.commands',
 'cli.tests.decorators',
 'cli.tests.helpers',
 'cli.tests.helpers.ec2',
 'cli.tests.helpers.updater',
 'cli.tests.integration',
 'cli.tests.saml_clients']

package_data = \
{'': ['*'], 'cli.tests.helpers.updater': ['responses/*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'SecretStorage>=3.2.0,<4.0.0',
 'analytics-python>=1.3.1,<2.0.0',
 'boto3>=1.16.20,<2.0.0',
 'click-option-group>=0.5.1,<0.6.0',
 'click>=8.0.0,<9.0.0',
 'colorama<0.4.4',
 'cryptography<3.4',
 'immutables>=0.14,<0.15',
 'keyring>=21.5.0,<22.0.0',
 'mistune<2.0.0',
 'policyuniverse>=1.3.2,<2.0.0',
 'portalocker>=2.0.0,<3.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.25,<3.0',
 'semver>=2.13.0,<3.0.0',
 'sentry-sdk>=0.19.3,<0.20.0',
 'sym-shared-cli>=0.2.2,<0.3.0',
 'validators>=0.18.1,<0.19.0']

entry_points = \
{'console_scripts': ['sym = sym.cli.sym:sym']}

setup_kwargs = {
    'name': 'sym-cli',
    'version': '0.2.9',
    'description': "Sym's Official CLI for Users",
    'long_description': '# sym-cli\n\nThis is the official CLI for [Sym](https://symops.com/) Users. Check out the docs [here](https://docs.symops.com/docs/install-sym-cli).\n',
    'author': 'SymOps, Inc.',
    'author_email': 'pypi@symops.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://symops.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
