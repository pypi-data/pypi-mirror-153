# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydantic_pynamodb']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0', 'pynamodb>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'pydantic-pynamodb',
    'version': '0.0.5',
    'description': 'Pydantic Pynamodb',
    'long_description': "Pydantic Pynamodb\n=================\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/pydantic-pynamodb.svg\n   :target: https://pypi.org/project/pydantic-pynamodb/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/pydantic-pynamodb.svg\n   :target: https://pypi.org/project/pydantic-pynamodb/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/pydantic-pynamodb\n   :target: https://pypi.org/project/pydantic-pynamodb\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/pydantic-pynamodb\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/pydantic-pynamodb/latest.svg?label=Read%20the%20Docs\n   :target: https://pydantic-pynamodb.readthedocs.io/\n   :alt: Read the documentation at https://pydantic-pynamodb.readthedocs.io/\n.. |Tests| image:: https://github.com/andrewthetechie/pydantic-pynamodb/workflows/Tests/badge.svg\n   :target: https://github.com/andrewthetechie/pydantic-pynamodb/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/andrewthetechie/pydantic-pynamodb/branch/main/graph/badge.svg\n   :target: https://app.codecov.io/gh/andrewthetechie/pydantic-pynamodb\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\nWrap pynamo models in pydantic schemas to make them easy to work with in FastAPI.\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* pydantic\n* pynamodb\n\n\nInstallation\n------------\n\nYou can install *Pydantic Pynamodb* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install pydantic-pynamodb\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Pydantic Pynamodb* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/andrewthetechie/pydantic-pynamodb/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: https://pydantic-pynamodb.readthedocs.io/en/latest/contributing.html\n.. _Usage: https://pydantic-pynamodb.readthedocs.io/en/latest/usage.html\n",
    'author': 'Andrew Herrington',
    'author_email': 'andrew.the.techie@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andrewthetechie/pydantic-pynamodb',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
