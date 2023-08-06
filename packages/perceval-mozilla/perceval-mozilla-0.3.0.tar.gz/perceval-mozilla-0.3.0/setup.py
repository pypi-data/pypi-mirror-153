# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perceval', 'perceval.backends.mozilla', 'tests', 'tests.data.crates']

package_data = \
{'': ['*'], 'tests': ['data/kitsune/*', 'data/mozillaclub/*', 'data/remo/*']}

install_requires = \
['grimoirelab-toolkit>=0.3,<0.4',
 'perceval>=0.18,<0.19',
 'requests>=2.7.0,<3.0.0']

setup_kwargs = {
    'name': 'perceval-mozilla',
    'version': '0.3.0',
    'description': 'Bundle of Perceval backends for Mozilla ecosystem.',
    'long_description': '# perceval-mozilla [![Build Status](https://github.com/chaoss/grimoirelab-perceval-mozilla/workflows/tests/badge.svg)](https://github.com/chaoss/grimoirelab-perceval-mozilla/actions?query=workflow:tests+branch:master+event:push) [![Coverage Status](https://img.shields.io/coveralls/chaoss/grimoirelab-perceval-mozilla.svg)](https://coveralls.io/r/chaoss/grimoirelab-perceval-mozilla?branch=master)[![PyPI version](https://badge.fury.io/py/perceval-mozilla.svg)](https://badge.fury.io/py/perceval-mozilla)\n\nBundle of Perceval backends for Mozilla ecosystem.\n\n## Backends\n\nThe backends currently managed by this package support the next repositories:\n\n* Crates\n* Kitsune\n* MozillaClub\n* ReMo\n\n## Requirements\n\nThese set of backends requires Python 3.7 or later, and\n[Perceval](https://github.com/chaoss/grimoirelab-perceval/) to run.\nFor other Python dependencies, please check the `pyproject.toml`\nfile included on this repository.\n\n## Installation\n\nTo install this package you will need to clone the repository first:\n\n```\n$ git clone https://github.com/grimoirelab/perceval-mozilla.git\n```\n\nThen you can execute the following commands:\n```\n$ pip3 install -r requirements.txt\n$ pip3 install -e .\n```\n\nIn case you are a developer, you should execute the following commands to install Perceval in your working directory (option `-e`) and the packages of requirements_tests.txt.\n```\n$ pip3 install -r requirements.txt\n$ pip3 install -r requirements_test.txt\n$ pip3 install -e .\n```\n\n## Examples\n\n### Crates\n\n```\n$ perceval crates\n```\n\n### Kitsune\n\n```\n$ perceval kitsune --offset 373990\n```\n\n### Mozilla Club Events\n\n```\n$ perceval mozillaclub\n```\n\n### ReMo\n```\n$ perceval remo\n```\n\n## License\n\nLicensed under GNU General Public License (GPL), version 3 or later.\n',
    'author': 'GrimoireLab Developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://chaoss.github.io/grimoirelab/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
