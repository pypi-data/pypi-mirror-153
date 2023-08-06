# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['motor-stubs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'motor-stubs',
    'version': '1.4.0',
    'description': '',
    'long_description': '# Motor Stubs\n\nExperimental stubs for [motor](https://pypi.org/project/motor/).\n\n\n**motor-stubs is NOT an officially supported MongoDB product.**\n\n\n## Installation\n\n`motor-stubs` can be installed with [pip](https://pypi.org/project/pip/)\n\n```shell\npip install motor-stubs\n```\n\n## Dependencies\n\n- Python >= 3.9\n- Motor >= 3.0.0, < 4.0\n\n## Note\n\n1. You should not use this stubs package after the official `motor` package supports inline type annotations.\n2. File [generator.py](/generator.py) can help to parse class `AgnosticCollection` and `AgnosticDatabase`,\n   other class might not work\n\n### Usage `generator.py`\n\n```python\n# at the project root, and get into python shell\nfrom motor.core import AgnosticCollection\nfrom generator import gen\n\ngen(AgnosticCollection)\n```\n\nIt will output a file in folder `pyi_tmp/`.\n\n## Support / Feedback\n\nmotor-stubs is experimental and is not an officially supported MongoDB product.\nFor questions, discussions, or general technical support, visit the [MongoDB Community Forums](https://developer.mongodb.com/community/forums/tag/python).\n',
    'author': 'Daniel Hsiao',
    'author_email': 'yian8068@yahoo.com.tw',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Yian8068/motor-stubs.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
