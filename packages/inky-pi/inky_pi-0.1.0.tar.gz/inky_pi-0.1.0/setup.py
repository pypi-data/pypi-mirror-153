# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inky_pi',
 'inky_pi.display',
 'inky_pi.display.util',
 'inky_pi.train',
 'inky_pi.weather',
 'tests',
 'tests.e2e',
 'tests.unit',
 'tests.unit.resources']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'click>=8.1.2,<9.0.0',
 'environs>=9.3.2,<10.0.0',
 'font-fredoka-one>=0.0.4,<0.0.5',
 'font-hanken-grotesk>=0.0.2,<0.0.3',
 'loguru>=0.5.3,<0.6.0',
 'numpy==1.21.1',
 'rich>=12.4.1,<13.0.0',
 'urllib3>=1.26.8,<2.0.0',
 'zeep>=4.0.0,<5.0.0']

extras_require = \
{':platform_machine == "armv7l"': ['RPi.GPIO>=0.7.0,<0.8.0',
                                   'inky>=1.2.0,<2.0.0']}

entry_points = \
{'console_scripts': ['inky_pi = inky_pi.cli:main']}

setup_kwargs = {
    'name': 'inky-pi',
    'version': '0.1.0',
    'description': 'Top-level package for inky-pi.',
    'long_description': '=======\ninky-pi\n=======\n\n\n.. image:: https://img.shields.io/pypi/v/inky_pi.svg\n        :target: https://pypi.python.org/pypi/inky_pi\n\n.. image:: https://github.com/mickeykkim/inky_pi/actions/workflows/main.yml/badge.svg\n        :target: https://github.com/mickeykkim/inky_pi/actions/workflows/main.yml\n\n.. image:: https://readthedocs.org/projects/inky-pi/badge/?version=latest\n        :target: https://inky-pi.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\nThis program generates weather and UK train data for output to various displays (inkyWHAT e-ink display, terminal, desktop png).\n\n\n* Free software: MIT\n* Documentation: https://inky-pi.readthedocs.io.\n\n\nFeatures\n--------\n\n* Displays weather data using Weather Underground API\n* Displays UK train data using National Rail API\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Mickey Kim',
    'author_email': 'mickeykkim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mickeykkim/inky_pi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
