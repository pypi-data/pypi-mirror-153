# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cookiecutter_hypermodern_python_instance']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1']

entry_points = \
{'console_scripts': ['cookiecutter-hypermodern-python-instance = '
                     'cookiecutter_hypermodern_python_instance.__main__:main']}

setup_kwargs = {
    'name': 'cookiecutter-hypermodern-python-instance',
    'version': '2022.6.3',
    'description': 'Cookiecutter Hypermodern Python Instance',
    'long_description': "# Cookiecutter Hypermodern Python Instance\n\n[![PyPI](https://img.shields.io/pypi/v/cookiecutter-hypermodern-python-instance.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/cookiecutter-hypermodern-python-instance.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/cookiecutter-hypermodern-python-instance)][python version]\n[![License](https://img.shields.io/pypi/l/cookiecutter-hypermodern-python-instance)][license]\n\n[![Read the documentation at https://cookiecutter-hypermodern-python-instance.readthedocs.io/](https://img.shields.io/readthedocs/cookiecutter-hypermodern-python-instance/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/cjolowicz/cookiecutter-hypermodern-python-instance/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/cookiecutter-hypermodern-python-instance/\n[status]: https://pypi.org/project/cookiecutter-hypermodern-python-instance/\n[python version]: https://pypi.org/project/cookiecutter-hypermodern-python-instance\n[read the docs]: https://cookiecutter-hypermodern-python-instance.readthedocs.io/\n[tests]: https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/cjolowicz/cookiecutter-hypermodern-python-instance\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Cookiecutter Hypermodern Python Instance_ via [pip] from [PyPI]:\n\n```console\n$ pip install cookiecutter-hypermodern-python-instance\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Cookiecutter Hypermodern Python Instance_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/blob/main/LICENSE\n[contributor guide]: https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance/blob/main/CONTRIBUTING.md\n[command-line reference]: https://cookiecutter-hypermodern-python-instance.readthedocs.io/en/latest/usage.html\n",
    'author': 'Claudio Jolowicz',
    'author_email': 'mail@claudiojolowicz.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cjolowicz/cookiecutter-hypermodern-python-instance',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
