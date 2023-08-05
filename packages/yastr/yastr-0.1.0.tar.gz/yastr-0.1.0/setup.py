# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yastr']

package_data = \
{'': ['*']}

install_requires = \
['anyconfig[template,yaml]>=0.13.0,<0.14.0',
 'marshmallow-dataclass[union]>=8.5.3,<9.0.0',
 'pytest>=7.1.1,<8.0.0',
 'wrapt>=1.14.0,<2.0.0']

entry_points = \
{'console_scripts': ['yastr = yastr:main']}

setup_kwargs = {
    'name': 'yastr',
    'version': '0.1.0',
    'description': 'Yet another simple test runner',
    'long_description': '<div align="center">\n  <br>\n  <img src="https://raw.githubusercontent.com/codetent/yastr/main/doc/logo.svg" width="100" /><br>\n  \n  # <b>Y</b>et <b>A</b>nother <b>S</b>imple <b>T</b>est <b>R</b>unner\n  \n  A simple test runner for just calling executables and generating reports.\n  <br/><br/>\n</div>\n\n![PyPI](https://img.shields.io/pypi/v/yastr)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yastr)\n![PyPI - License](https://img.shields.io/pypi/l/yastr)\n[![Python package](https://github.com/codetent/yastr/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/codetent/yastr/actions/workflows/python-package.yml)\n[![Packaging](https://github.com/codetent/yastr/actions/workflows/packaging.yml/badge.svg?branch=main)](https://github.com/codetent/yastr/actions/workflows/packaging.yml)\n\n## Description\n\nYASTR is a utility that gets the testing job quickly done without requiring a specific test framework. Instead just having an executable that shall be executed is enough.\n\nIn its simplest configuration, you just place your executable containing your test logic in a folder, create a configuration file to tell yastr how to execute it and you get a nice JUnit compatible output.\n\nIt is based on pytest, actually a testing framework for Python but not limited to. Thanks to it, yastr is able to run beside executables also Python tests and features like fixtures and markers can be reused.\n\n## Features\n\nYASTR provides the following:\n\n- Running executables with arguments\n- Settings environment variables\n- Setting a timeout\n\nAnd it supports everything that pytest offers:\n\n- Creating Junit reports\n- Adding markers\n- Using fixtures\n- Selecting specific tests\n- Running tests written in Python\n- And much more: https://docs.pytest.org/en/6.2.x/contents.html\n\n## Documentation\n\n- Quickstart: [doc/guide/quickstart.md](https://github.com/codetent/yastr/blob/main/doc/guide/quickstart.md)\n- Advanced: [doc/guide/advanced.md](https://github.com/codetent/yastr/blob/main/doc/guide/advanced.md)\n\n## Installation\n\n### Python\n\n```bash\n$ pip install yastr\n```\n',
    'author': 'Christoph Swoboda',
    'author_email': 'codetent@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/codetent/yastr',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
