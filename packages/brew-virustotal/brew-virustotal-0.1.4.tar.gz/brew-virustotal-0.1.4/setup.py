# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brew_virustotal']

package_data = \
{'': ['*']}

install_requires = \
['virustotal-tddschn>=0.1.6,<0.2.0']

entry_points = \
{'console_scripts': ['brew-vt = brew_virustotal.cli:main']}

setup_kwargs = {
    'name': 'brew-virustotal',
    'version': '0.1.4',
    'description': 'Check Homebrew formulae and casks with VirusTotal',
    'long_description': '',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tddschn/brew-virustotal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
