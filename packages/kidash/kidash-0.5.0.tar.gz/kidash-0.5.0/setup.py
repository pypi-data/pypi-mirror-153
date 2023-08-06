# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kidash', 'kidash.bin', 'tests']

package_data = \
{'': ['*'], 'tests': ['data/*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0', 'requests==2.26.0', 'urllib3==1.26.5']

entry_points = \
{'console_scripts': ['kidash = kidash.bin.kidash:main']}

setup_kwargs = {
    'name': 'kidash',
    'version': '0.5.0',
    'description': 'GrimoireLab script to manage Kibana dashboards from the command line',
    'long_description': '# Kidash [![Build Status](https://github.com/chaoss/grimoirelab-kidash/workflows/tests/badge.svg)](https://github.com/chaoss/grimoirelab-kidash/actions?query=workflow:tests+branch:master+event:push) [![Coverage Status](https://img.shields.io/coveralls/chaoss/grimoirelab-kidash.svg)](https://coveralls.io/r/chaoss/grimoirelab-kidash?branch=master)\n\nKidash is a tool for managing Kibana-related dashboards from the command line. The standard GrimoireLab dashboards\nare available in the [Sigils](https://github.com/chaoss/grimoirelab-sigils) repository.\n\n## Installation\n\nYou can set up a virtual environment where Kidash will be installed\n```\npython3 -m venv foo\nsource bin foo/bin/activate\n```\n\n* Using PyPi\n```buildoutcfg\npip3 install kidash\n```\n\n* From Source code\n```buildoutcfg\ngit clone https://github.com/chaoss/grimoirelab-kidash\ncd grimoirelab-kidash\npython3 setup.py install\n```\n\n## Usage\n\n- Get a list of all options with:\n```\n$ kidash --help\n```\n\n- Import a dashboard:\n```buildoutcfg\nkidash -g -e <elasticsearch-url>:<port> --import <local-file-path>\nexample: kidash -g -e https://admin:admin@localhost:9200 --import ./overview.json\n```\n\n- Export a dashboard:\n```buildoutcfg\nkidash -g -e <elasticsearch-url> --dashboard <dashboard-id>* --export <local-file-path> --split-index-pattern\nexample: kidash -g -e https://admin:admin@localhost:9200 --dashboard overview --export overview.json\n```\n',
    'author': 'GrimoireLab Developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://chaoss.github.io/grimoirelab/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
