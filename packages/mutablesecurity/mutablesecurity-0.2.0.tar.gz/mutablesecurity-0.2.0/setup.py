# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mutablesecurity',
 'mutablesecurity.modules',
 'mutablesecurity.modules.helpers',
 'mutablesecurity.modules.leader',
 'mutablesecurity.modules.main',
 'mutablesecurity.modules.solutions_manager',
 'mutablesecurity.modules.solutions_manager.deployments',
 'mutablesecurity.modules.solutions_manager.facts',
 'mutablesecurity.modules.solutions_manager.solutions']

package_data = \
{'': ['*'],
 'mutablesecurity.modules.solutions_manager': ['files/*', 'files/teler/*']}

install_requires = \
['Click>=8.0,<9.0',
 'PyYAML==6.0',
 'humanfriendly>=10.0,<11.0',
 'packaging>=21.3,<22.0',
 'pyinfra>=1.6.1,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich==11.2.0']

entry_points = \
{'console_scripts': ['mutablesecurity = mutablesecurity.cli:main']}

setup_kwargs = {
    'name': 'mutablesecurity',
    'version': '0.2.0',
    'description': 'Seamless deployment and management of cybersecurity solutions',
    'long_description': '<div align="center">\n    <img src="https://raw.githubusercontent.com/MutableSecurity/mutablesecurity/main/others/cover.png" width="600px" alt="Cover">\n</div>\n\n<br>\n\n---\n\n# Background 👴🏼\n\nIn today\'s fast-paced society, most people are unaware of the potential consequences of cyberattacks on their organizations. Furthermore, they do not invest in cybersecurity solutions due to the costs of setup, licensing, and maintenance.\n\n# Vision 📜\n\n**MutableSecurity** 🏗️ is a software product for making cybersecurity solution management easier and more accessible, from deployment and configuration to monitoring.\n\nDespite the current lack of complex functionalities, we have a vision in mind that we hope to achieve in the near future. As we must begin somewhere, the first step in our progress is this command line interface for automatic management of cybersecurity solutions.\n\nCome join the MutableSecurity journey!\n\n# Read Further 📎\n\nThis is only an excerpt from the `README.md` hosted on GitHub. To read the full text, please visit our [official repository](https://github.com/MutableSecurity/mutablesecurity)!',
    'author': 'MutableSecurity',
    'author_email': 'hello@mutablesecurity.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.mutablesecurity.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
