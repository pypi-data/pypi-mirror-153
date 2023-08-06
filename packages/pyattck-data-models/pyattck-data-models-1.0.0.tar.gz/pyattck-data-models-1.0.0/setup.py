# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyattck_data_models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.4.0,<22.0.0', 'click>=8.0.1,<9.0.0', 'pydantic>=1.9.1,<2.0.0']

entry_points = \
{'console_scripts': ['pyattck-data-models = pyattck_data_models.__main__:main']}

setup_kwargs = {
    'name': 'pyattck-data-models',
    'version': '1.0.0',
    'description': 'Pyattck Data models',
    'long_description': '# pyattck-data-models\n\n<a href="https://pypi.org/project/pyattck-data-models/"><img src="https://img.shields.io/pypi/v/pyattck-data-models.svg" alt="PyPI" style="float: left; margin-right: 10px;" /></a>\n<a href="https://pypi.org/project/pyattck-data-models/"><img src="https://img.shields.io/pypi/status/pyattck-data-models.svg" alt="Status" style="float: left; margin-right: 10px;" /></a>\n<a href="https://pypi.org/project/pyattck-data-models/"><img src="https://img.shields.io/pypi/pyversions/pyattck-data-models" alt="Python Version" style="float: left; margin-right: 10px;" /></a>\n<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/pypi/l/pyattck-data-models" alt="License" style="float: left; margin-right: 10px;" /></a>\n<a href="https://github.com/swimlane/pyattck-data-models/actions?workflow=Tests"><img src="https://github.com/swimlane/pyattck-data-models/workflows/Tests/badge.svg" alt="Tests" style="float: left; margin-right: 10px;" /></a>\n<a href="https://codecov.io/gh/swimlane/pyattck-data-models"><img src="https://codecov.io/gh/swimlane/pyattck-data-models/branch/main/graph/badge.svg" alt="Codecov" style="float: left; margin-right: 10px;" /></a>\n<a href="https://github.com/pre-commit/pre-commit"><img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="pre-commit" style="float: left; margin-right: 10px;" /></a>\n<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black" style="float: left; margin-right: 10px;" /></a>\n\n# \n\n## Features\n\nIncludes data models for the following projects:\n\n* [pyattck](https://github.com/swimlane/pyattck/)\n* [pyattck-data](https://github.com/swimlane/pyattck-data/)\n\n\n## Installation\n\nYou can install *Pyattck Data Models* via pip_ from PyPI_:\n\n```\n$ pip install pyattck-data-models\n```\n\n##Usage\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\n## License\n\nDistributed under the terms of the `MIT license`_,\n*Pyattck Data Models* is free and open source software.\n\n\n## Issues\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n',
    'author': 'Swimlane',
    'author_email': 'info@swimlane.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/swimlane/pyattck-data-models',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
