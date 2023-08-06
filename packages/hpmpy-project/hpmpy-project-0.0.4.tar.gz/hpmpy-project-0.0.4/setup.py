# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hpmpy_project']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'hpmpy-project',
    'version': '0.0.4',
    'description': 'Tweaked Hypermodern Python Project Template w/o Typing',
    'long_description': 'hpmpy-project\n====================================================================================================\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov| |Codacy| |Codeclimate| |Scrutinizer|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/hpmpy-project.svg\n   :target: https://pypi.org/project/hpmpy-project/\n   :alt: PyPI\n\n.. |Status| image:: https://img.shields.io/pypi/status/hpmpy-project.svg\n   :target: https://pypi.org/project/hpmpy-project/\n   :alt: Status\n\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/hpmpy-project\n   :target: https://pypi.org/project/hpmpy-project\n   :alt: Python Version\n\n.. |License| image:: https://img.shields.io/pypi/l/hpmpy-project\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/hpmpy-project/latest.svg?label=Read%20the%20Docs\n   :target: https://hpmpy-project.readthedocs.io/\n   :alt: Read the documentation at https://hpmpy-project.readthedocs.io/\n\n.. |Tests| image:: https://github.com/tZ3ma/hpmpy-project/workflows/Tests/badge.svg\n   :target: https://github.com/tZ3ma/hpmpy-project/actions?workflow=Tests\n   :alt: Tests\n\n.. |Codecov| image:: https://codecov.io/gh/tZ3ma/hpmpy-project/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/tZ3ma/hpmpy-project\n   :alt: Codecov\n\n.. |Codacy| image:: https://app.codacy.com/project/badge/Grade/b278433bb9224147a2e6231d783b62e4\n   :target: https://app.codacy.com/gh/tZ3ma/hpmpy-project/dashboard\n   :alt: Codacy Code Quality Status\n\n.. |Codeclimate| image:: https://api.codeclimate.com/v1/badges/ff119252f0bb7f40aecb/maintainability\n   :target: https://codeclimate.com/github/tZ3ma/hpmpy-project/maintainability\n   :alt: Maintainability\n\n.. |Scrutinizer| image:: https://scrutinizer-ci.com/g/tZ3ma/hpmpy-project/badges/quality-score.png?b=main\n   :target: https://scrutinizer-ci.com/g/tZ3ma/hpmpy-project/\n   :alt: Scrutinizer Code Quality\n\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\nNewb tweaked non-typing version of the excellent Hypermodern-Python_ project\nfoundation proposed by `Claudio Jolowicz <cj>`_\n\nInstallation\n------------\n\nFollow the `Installation Guide`_.\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*hpmpy-project* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\nCredits\n-------\n\nThis project was created using the `Mathias Ammon <tZ3ma>`_ tweaked version of the\nHypermodern-Python_ project foundation proposed by `Claudio Jolowicz <cj>`_.\n\n.. _Hypermodern-Python: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _cj: https://github.com/cjolowicz\n\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n\n.. _file an issue: https://github.com/tZ3ma/hpmpy-project/issues\n.. _pip: https://pip.pypa.io/\n\n.. _tZ3ma: https://github.com/tZ3ma\n.. working on github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Installation Guide: docs/source/getting_started/installation.rst\n',
    'author': 'Mathias Ammon',
    'author_email': 'mathias.ammon@tuhh.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tZ3ma/hpmpy_project',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
