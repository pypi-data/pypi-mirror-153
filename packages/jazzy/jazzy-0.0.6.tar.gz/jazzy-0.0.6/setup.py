# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jazzy']

package_data = \
{'': ['*']}

install_requires = \
['click<8.0.0', 'kallisto>=1.0.7,<2.0.0', 'rdkit-pypi<=2021.9.4']

entry_points = \
{'console_scripts': ['jazzy = jazzy.__main__:cli']}

setup_kwargs = {
    'name': 'jazzy',
    'version': '0.0.6',
    'description': 'Jazzy',
    'long_description': ".. image:: https://raw.githubusercontent.com/AstraZeneca/jazzy/master/docs/_static/jazzy.png\n  :width: 400\n  :alt: Jazzy\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/jazzy.svg\n   :target: https://pypi.org/project/jazzy/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/jazzy.svg\n   :target: https://pypi.org/project/jazzy/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/jazzy\n   :target: https://pypi.org/project/jazzy\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/jazzy\n   :target: https://opensource.org/licenses/Apache-2.0\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/jazzy/latest.svg?label=Read%20the%20Docs\n   :target: https://jazzy.readthedocs.io/\n   :alt: Read the documentation at https://jazzy.readthedocs.io/\n.. |Tests| image:: https://github.com/AstraZeneca/jazzy/workflows/Tests/badge.svg\n   :target: https://github.com/AstraZeneca/jazzy/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/AstraZeneca/jazzy/branch/master/graph/badge.svg?token=4HCWYH61S5\n   :target: https://codecov.io/gh/AstraZeneca/jazzy\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\nFull Author List\n----------------\n* Eike Caldeweyher\n* Gian Marco Ghiandoni\n\n\nIntroduction\n------------\n*Jazzy* is an efficient computational tool for the calculation of hydration free energies and hydrogen bond acceptor and donor strengths.\n\n\nFeatures\n--------\n\n* Hydration free energies\n* Hydrogen bond strengths\n* Visualisation functions (SVG)\n* Application programming interface\n* Command-line interface\n\n\nRequirements\n------------\n\n.. code:: console\n\n   click==7.1.2            # Composable command line interface toolkit\n   kallisto==1.0.7         # Atomic and molecular featurizer\n   numpy==1.21.1           # NumPy array computing package\n   rdkit-pypi<=2021.9.4    # Chemoinformatics toolkit\n\n\nInstallation\n------------\n\nYou can install *Jazzy* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install jazzy\n\n\nInstallation from Source\n------------------------\n\nRequirements to install *Jazzy* from sources:\n\n- `poetry`_\n- `pyenv`_ or `conda`_\n- python>=3.6\n\nFirst check that ``poetry`` is running correctly (v1.0.10 at the time of writing)\n\n.. code:: console\n\n   $ poetry --version\n   Poetry version 1.0.10\n\nCreate a virtual environment (via ``pyenv`` or ``conda``) and activate it. Afterwards, clone the *Jazzy* project from GitHub and install it using ``poetry``\n\n.. code:: console\n\n   $ git clone git@github.com:AstraZeneca/jazzy.git\n   $ cd jazzy\n   $ poetry install\n\n\nUsage and Cookbook\n------------------\n\nPlease see the `Usage <Usage_>`_ and `Cookbook <Cookbook_>`_ sections for details.\n\n\nContributing\n------------\n\nJazzy is an open project in every shape and form, thus feedback on how to improve its documentation or functionalities is always welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `Apache 2.0 license`_,\n*Jazzy* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _Apache 2.0 license: https://opensource.org/licenses/Apache-2.0\n.. _poetry: https://python-poetry.org/docs/#installation\n.. _pyenv: https://github.com/pyenv/pyenv#installation\n.. _conda: https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/AstraZeneca/jazzy/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: contributing.rst\n.. _Cookbook: https://jazzy.readthedocs.io/en/latest/cookbook.html\n.. _Usage: https://jazzy.readthedocs.io/en/latest/usage.html\n",
    'author': 'Gian Marco Ghiandoni',
    'author_email': 'ghiandoni.g@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AstraZeneca/jazzy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
