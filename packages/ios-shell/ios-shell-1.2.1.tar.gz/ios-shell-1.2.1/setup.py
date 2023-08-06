# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ios_shell']

package_data = \
{'': ['*']}

install_requires = \
['fortranformat>=1.0.1,<2.0.0']

extras_require = \
{'pandas': ['pandas>=1.4.2,<2.0.0']}

setup_kwargs = {
    'name': 'ios-shell',
    'version': '1.2.1',
    'description': "Parses files formatted by the Institute of Ocean Sciences' IOSShell tool",
    'long_description': '# IOS Shell file parsing library\n\nThis is a library for parsing files in the IOS Shell format.\nIt has no relation to iOS or terminal shells.\n\n## Prerequisites\n\n- Python 3.8, 3.9, or 3.10 with pip\n\n## Example\n\nIf `1930-003-0058.bot` is in the same folder as the program using ios_shell:\n\n    parsed_file = ios_shell.ShellFile.fromfile("1930-003-0058.bot")\n\nTo use the contents of a file previously read into the program:\n\n    parsed_contents = ios_shell.ShellFile.fromcontents(contents)\n',
    'author': 'James Hannah',
    'author_email': 'jhannah@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cyborgsphinx/ios-shell',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
