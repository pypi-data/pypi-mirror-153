# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['longprocess']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'longprocess',
    'version': '0.1.1',
    'description': '',
    'long_description': '# `longprocess`\n\nUtilities for running processes that take a long time. \n\nCall `linger()` to prevent a process from exiting when its terminal is closed.\nCall `evesdrop(out_file: str, targets: List[TextIO] = [sys.stdout, sys.stdout])` to tee the output to a file, to keep track of what happens after.',
    'author': 'yohan-pg',
    'author_email': 'pg.yohan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
