# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ghdl']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'hy>=1.0a4,<2.0',
 'hyrule>=0.1,<0.2',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-magic>=0.4.25,<0.5.0',
 'requests>=2.27.1,<3.0.0',
 'xdg>=4.0.1,<5.0.0',
 'xtract>=0.1a3,<0.1']

scripts = \
['bin/ghdl', 'bin/ghdl-delete-repo']

setup_kwargs = {
    'name': 'ghdl',
    'version': '0.3.2',
    'description': 'Package manager for Github Release binaries',
    'long_description': 'None',
    'author': 'Imran Khan',
    'author_email': 'contact@imrankhan.live',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'scripts': scripts,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
