# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tsrc', 'tsrc.cli', 'tsrc.test', 'tsrc.test.cli', 'tsrc.test.helpers']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'cli-ui>=0.11.0,<0.12.0',
 'colored_traceback>=0.3.0,<0.4.0',
 'ruamel.yaml>=0.16.7,<0.17.0',
 'schema>=0.7.1,<0.8.0',
 'tabulate>=0.8.6,<0.9.0',
 'unidecode>=1.1.1,<2.0.0']

entry_points = \
{'console_scripts': ['tsrc = tsrc.cli.main:main']}

setup_kwargs = {
    'name': 'tsrc',
    'version': '2.7.1',
    'description': 'Manage groups of git repositories',
    'long_description': '.. image:: https://img.shields.io/github/license/dmerejkowsky/tsrc.svg\n   :target: https://github.com/dmerejkowsky/tsrc/blob/main/LICENSE\n\n.. image:: https://github.com/dmerejkowsky/tsrc/workflows/tests/badge.svg\n   :target: https://github.com/dmerejkowsky/tsrc/actions\n\n.. image:: https://github.com/dmerejkowsky/tsrc/workflows/linters/badge.svg\n   :target: https://github.com/dmerejkowsky/tsrc/actions\n\n.. image:: https://img.shields.io/pypi/v/tsrc.svg\n   :target: https://pypi.org/project/tsrc/\n\n.. image:: https://img.shields.io/badge/deps%20scanning-pyup.io-green\n     :target: https://github.com/dmerejkowsky/tsrc/actions\n\ntsrc: manage groups of git repositories\n=======================================\n\n`Overview`_ · `Installation`_ · `Usage example`_ · `Documentation`_ · `Release notes`_ · `Contributing`_ · `License`_\n\nNote\n----\n\nThis project was originally hosted on the `TankerHQ\n<https://github.com/TankerHQ>`_ organization, which was my employer from 2016\nto 2021. They kindly agreed to give back ownership of this project to\nme. Thanks!\n\nOverview\n---------\n\ntsrc is a command-line tool that helps you manage groups of several git repositories.\n\nIt can be `seen in action on asciinema.org <https://asciinema.org/a/131625>`_.\n\nNote\n-----\n\n`tsrc` does not adhere strictly to the `semver specification <https://semver.org/>`_. So before upgrading to a new version, please take the time to read the `Changelog <https://dmerejkowsky.github.io/tsrc/changelog/>`_ first!\n\nInstallation\n-------------\n\nThe recommended way to install ``tsrc`` is to use `pipx <https://pipxproject.github.io/pipx/>`_\n\n* Make sure to have Python **3.7** or later installed.\n* Install ``pipx``\n* Run ``pipx install tsrc``.\n\n\nUsage Example\n-------------\n\n\n* Create a *manifest* repository. (``git@example.org/manifest``)\n\n* Push a file named ``manifest.yml`` looking like:\n\n.. code-block:: yaml\n\n    repos:\n      - url: git@example.com/foo.git\n        dest: foo\n\n     -  url: git@example.com/bar.git\n        dest: bar\n\n\n* Create a new workspace with all the repositories listed in the manifest:\n\n.. code-block:: console\n\n    $ tsrc init git@git.local/manifest.git\n\n    :: Configuring workspace in /path/to/work\n    ...\n    => Cloning missing repos\n    * (1/2) foo\n    ...\n    * (2/2) bar\n    ...\n    : Configuring remotes\n    Done ✓\n\n\n* Synchronize all the repositories in the workspace:\n\n.. code-block:: console\n\n    $ tsrc sync\n    => Updating manifest\n    ...\n    :: Configuring remotes\n    :: Synchronizing workspace\n    * (1/2) foo\n    => Fetching origin\n    => Updating branch\n    Already up to date\n    * (2/2) bar\n    => Updating branch\n    Updating 29ac0e1..b635a43\n    Fast-forward\n     bar.txt | 1 +\n     1 file changed, 1 insertion(+)\n     create mode 100644 bar.txt\n    Done ✓\n\n\nDocumentation\n--------------\n\nFor more details and examples, please refer to `tsrc documentation <https://dmerejkowsky.github.io/tsrc/>`_.\n\nRelease notes\n-------------\n\nDetailed changes for each release are documented in the `changelog <https://dmerejkowsky.github.io/tsrc/changelog/>`_.\n\nContributing\n------------\n\nWe welcome feedback, `bug reports <https://github.com/dmerejkowsky/tsrc/issues>`_, and bug fixes in the form of `pull requests <https://github.com/dmerejkowsky/tsrc/pulls>`_.\n\nDetailed instructions can be found `in the documentation <https://dmerejkowsky.github.io/tsrc>`_.\n\nLicense\n-------\n\ntsrc is licensed under a `BSD 3-Clause license <https://github.com/dmerejkowsky/tsrc/blob/main/LICENSE>`_.\n',
    'author': 'Dimitri Merejkowsky',
    'author_email': 'dimitri@dmerej.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dmerejkowsky/tsrc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
