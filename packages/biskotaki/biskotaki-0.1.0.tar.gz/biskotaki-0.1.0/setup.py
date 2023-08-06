# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['biskotaki']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['sphinx>=4.0,<5.0',
          'sphinx-autodoc-typehints>=1.10',
          'sphinx-rtd-theme==0.5.0',
          'sphinxcontrib-spelling>=7.3.3,<7.4.0'],
 'test': ['pytest>=6.2.4',
          'pytest-cov>=2.12',
          'pytest-explicit>=1.0.1,<1.1.0',
          'pytest-xdist>=1.34'],
 'typing': ['mypy>=0.950,<1.0']}

setup_kwargs = {
    'name': 'biskotaki',
    'version': '0.1.0',
    'description': 'Project generated from the https://github.com/boromir674/cookiecutter-python-package/tree/master/src/cookiecutter_python cookiecutter',
    'long_description': "BISKOTAKI\n\nProject generated from the https://github.com/boromir674/cookiecutter-python-package/tree/master/src/cookiecutter_python cookiecutter\n\n.. start-badges\n\n| |build| |docs| |coverage| |maintainability| |better_code_hub| |tech-debt|\n| |release_version| |wheel| |supported_versions| |gh-lic| |commits_since_specific_tag_on_master| |commits_since_latest_github_release|\n\n|\n| **Code:** https://github.com/boromir674/biskotaki\n| **Docs:** https://biskotaki.readthedocs.io/en/master/\n| **PyPI:** https://pypi.org/project/biskotaki/\n| **CI:** https://github.com/boromir674/biskotaki/actions/\n\n\nFeatures\n========\n\n1. **biskotaki** `python package`\n\n   a. TODO Document a **Great Feature**\n   b. TODO Document another **Nice Feature**\n2. Tested against multiple `platforms` and `python` versions\n\n\nDevelopment\n-----------\nHere are some useful notes related to doing development on this project.\n\n1. **Test Suite**, using `pytest`_, located in `tests` dir\n2. **Parallel Execution** of Unit Tests, on multiple cpu's\n3. **Documentation Pages**, hosted on `readthedocs` server, located in `docs` dir\n4. **Automation**, using `tox`_, driven by single `tox.ini` file\n\n   a. **Code Coverage** measuring\n   b. **Build Command**, using the `build`_ python package\n   c. **Pypi Deploy Command**, supporting upload to both `pypi.org`_ and `test.pypi.org`_ servers\n   d. **Type Check Command**, using `mypy`_\n   e. **Lint** *Check* and `Apply` commands, using `isort`_ and `black`_\n5. **CI Pipeline**, running on `Github Actions`_, defined in `.github/`\n\n   a. **Job Matrix**, spanning different `platform`'s and `python version`'s\n\n      1. Platforms: `ubuntu-latest`, `macos-latest`\n      2. Python Interpreters: `3.6`, `3.7`, `3.8`, `3.9`, `3.10`\n   b. **Parallel Job** execution, generated from the `matrix`, that runs the `Test Suite`\n\n\nPrerequisites\n=============\n\nYou need to have `Python` installed.\n\nQuickstart\n==========\n\nUsing `pip` is the approved way for installing `biskotaki`.\n\n.. code-block:: sh\n\n    python3 -m pip install biskotaki\n\n\nTODO Document a use case\n\n\nLicense\n=======\n\n|gh-lic|\n\n* `GNU Affero General Public License v3.0`_\n\n\nLicense\n=======\n\n* Free software: GNU Affero General Public License v3.0\n\n\n\n.. LINKS\n\n.. _tox: https://tox.wiki/en/latest/\n\n.. _pytest: https://docs.pytest.org/en/7.1.x/\n\n.. _build: https://github.com/pypa/build\n\n.. _pypi.org: https://pypi.org/\n\n.. _test.pypi.org: https://test.pypi.org/\n\n.. _mypy: https://mypy.readthedocs.io/en/stable/\n\n.. _isort: https://pycqa.github.io/isort/\n\n.. _black: https://black.readthedocs.io/en/stable/\n\n.. _Github Actions: https://github.com/boromir674/biskotaki/actions\n\n.. _GNU Affero General Public License v3.0: https://github.com/boromir674/biskotaki/blob/master/LICENSE\n\n\n.. BADGE ALIASES\n\n.. Build Status\n.. Github Actions: Test Workflow Status for specific branch <branch>\n\n.. |build| image:: https://img.shields.io/github/workflow/status/boromir674/biskotaki/Test%20Python%20Package/master?label=build&logo=github-actions&logoColor=%233392FF\n    :alt: GitHub Workflow Status (branch)\n    :target: https://github.com/boromir674/biskotaki/actions/workflows/test.yaml?query=branch%3Amaster\n\n\n.. Documentation\n\n.. |docs| image:: https://img.shields.io/readthedocs/biskotaki/master?logo=readthedocs&logoColor=lightblue\n    :alt: Read the Docs (version)\n    :target: https://biskotaki.readthedocs.io/en/master/\n\n.. Code Coverage\n\n.. |coverage| image:: https://img.shields.io/codecov/c/github/boromir674/biskotaki/master?logo=codecov\n    :alt: Codecov\n    :target: https://app.codecov.io/gh/boromir674/biskotaki\n\n.. PyPI\n\n.. |release_version| image:: https://img.shields.io/pypi/v/biskotaki\n    :alt: Production Version\n    :target: https://pypi.org/project/biskotaki/\n\n.. |wheel| image:: https://img.shields.io/pypi/wheel/biskotaki?color=green&label=wheel\n    :alt: PyPI - Wheel\n    :target: https://pypi.org/project/biskotaki\n\n.. |supported_versions| image:: https://img.shields.io/pypi/pyversions/biskotaki?color=blue&label=python&logo=python&logoColor=%23ccccff\n    :alt: Supported Python versions\n    :target: https://pypi.org/project/biskotaki\n\n.. Github Releases & Tags\n\n.. |commits_since_specific_tag_on_master| image:: https://img.shields.io/github/commits-since/boromir674/biskotaki/v0.1.0/master?color=blue&logo=github\n    :alt: GitHub commits since tagged version (branch)\n    :target: https://github.com/boromir674/biskotaki/compare/v0.1.0..master\n\n.. |commits_since_latest_github_release| image:: https://img.shields.io/github/commits-since/boromir674/biskotaki/latest?color=blue&logo=semver&sort=semver\n    :alt: GitHub commits since latest release (by SemVer)\n\n.. LICENSE (eg AGPL, MIT)\n.. Github License\n\n.. |gh-lic| image:: https://img.shields.io/github/license/boromir674/biskotaki\n    :alt: GitHub\n    :target: https://github.com/boromir674/biskotaki/blob/master/LICENSE\n\n\n.. CODE QUALITY\n\n.. Better Code Hub\n.. Software Design Patterns\n\n.. |better_code_hub| image:: https://bettercodehub.com/edge/badge/boromir674/biskotaki?branch=master\n    :alt: Better Code Hub\n    :target: https://bettercodehub.com/\n\n\n.. Code Climate CI\n.. Code maintainability & Technical Debt\n\n.. |maintainability| image:: https://img.shields.io/codeclimate/maintainability/boromir674/biskotaki\n    :alt: Code Climate Maintainability\n    :target: https://codeclimate.com/github/boromir674/biskotaki/maintainability\n\n.. |tech-debt| image:: https://img.shields.io/codeclimate/tech-debt/boromir674/biskotaki\n    :alt: Technical Debt\n    :target: https://codeclimate.com/github/boromir674/biskotaki/maintainability\n",
    'author': 'Konstantinos Lampridis',
    'author_email': 'k.lampridis@hotmail.com',
    'maintainer': 'Konstantinos Lampridis',
    'maintainer_email': 'k.lampridis@hotmail.com',
    'url': 'https://github.com/boromir674/biskotaki',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
