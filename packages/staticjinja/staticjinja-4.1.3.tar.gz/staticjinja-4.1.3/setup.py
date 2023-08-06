# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['staticjinja']

package_data = \
{'': ['*']}

install_requires = \
['docopt-ng>=0.7.2', 'easywatch>=0.0.5,<0.0.6', 'jinja2>=2.10.1']

extras_require = \
{'dev': ['black>=21.12b0,<22.0',
         'flake8>=3.8.4,<4.0.0',
         'markdown>=3.3.3,<4.0.0',
         'pytest>=6.0.0,<7.0.0',
         'pytest-check>=1.0.1,<2.0.0',
         'pytest-cov>=2.5,<3.0',
         'sphinx>=4.1.1,<5.0.0',
         'sphinx-rtd-theme>=0.5.1,<0.6.0',
         'tomlkit>=0.5.8,<0.6.0',
         'tox>=3.0.0,<4.0.0',
         'twine>=3.3.0,<4.0.0']}

entry_points = \
{'console_scripts': ['staticjinja = staticjinja.cli:main']}

setup_kwargs = {
    'name': 'staticjinja',
    'version': '4.1.3',
    'description': 'jinja based static site generator',
    'long_description': "staticjinja\n===========\n\n.. image:: https://badge.fury.io/py/staticjinja.png\n    :target: https://badge.fury.io/py/staticjinja\n    :alt: PyPi Badge\n\n.. image:: https://github.com/staticjinja/staticjinja/workflows/build/badge.svg?branch=main&event=schedule\n    :target: https://github.com/staticjinja/staticjinja/actions?query=branch%3Amain\n    :alt: Build and Testing Status\n\n.. image:: https://readthedocs.org/projects/staticjinja/badge/?version=stable\n    :target: https://staticjinja.readthedocs.io/en/stable/?badge=stable&style=plastic\n    :alt: Documentation Status\n\n.. image:: https://codecov.io/gh/staticjinja/staticjinja/branch/main/graph/badge.svg?token=En337ZXsPK\n    :target: https://codecov.io/gh/staticjinja/staticjinja\n    :alt: Test coverage status\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: Code style: Black\n\n.. image:: https://static.pepy.tech/personalized-badge/staticjinja?period=total&units=international_system&left_color=black&right_color=blue&left_text=downloads\n    :target: https://pepy.tech/project/staticjinja\n    :alt: PyPi downloads total\n\n.. image:: https://static.pepy.tech/personalized-badge/staticjinja?period=month&units=international_system&left_color=black&right_color=blue&left_text=downloads/month\n    :target: https://pepy.tech/project/staticjinja\n    :alt: PyPi downloads per month\n\n**staticjinja** is a library that makes it easy to build static sites using\nJinja2_.\n\nMany static site generators are complex, with long manuals and unnecessary\nfeatures. But using template engines to build static websites is really useful.\n\nstaticjinja is designed to be lightweight (under 500 lines of source code),\nand to be easy to use, learn, and extend, enabling you to focus on making your\nsite.\n\n.. code-block:: bash\n\n    $ mkdir templates\n    $ vim templates/index.html\n    $ staticjinja watch\n    Building index.html...\n    Templates built.\n    Watching 'templates' for changes...\n    Press Ctrl+C to stop.\n\n\nInstallation\n------------\n\nTo install staticjinja, simply:\n\n.. code-block:: bash\n\n    $ pip install staticjinja\n\nDocumentation\n-------------\n\nDocumentation is available at\nhttps://staticjinja.readthedocs.io.\n\nContribute\n----------\n\nPlease see CONTRIBUTING_.\n\n.. _CONTRIBUTING: CONTRIBUTING.rst\n.. _Jinja2: https://jinja.palletsprojects.com\n",
    'author': 'Ceasar Bautista',
    'author_email': 'cbautista2010@gmail.com',
    'maintainer': 'Nick Crews',
    'maintainer_email': 'nicholas.b.crews@gmail.com',
    'url': 'https://github.com/staticjinja/staticjinja',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
