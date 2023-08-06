# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recline',
 'recline.arg_types',
 'recline.commands',
 'recline.formatters',
 'recline.repl',
 'recline.vendor',
 'recline.vendor.argcomplete',
 'recline.vendor.docstring_parser',
 'recline.vendor.docstring_parser.parser',
 'tests',
 'tests.test_arg_types',
 'tests.test_commands',
 'tests.test_formatters',
 'tests.test_repl']

package_data = \
{'': ['*'], 'recline.vendor.argcomplete': ['bash_completion.d/*']}

extras_require = \
{':sys_platform == "win32"': ['pyreadline>=2.1,<3.0',
                              'windows-curses>=2.3.0,<3.0.0']}

setup_kwargs = {
    'name': 'recline',
    'version': '2022.6',
    'description': 'Writing argparse-based command line applications can become tedious, repetitive, and difficult to do right. Relax and let this library free you from that burden.',
    'long_description': '![](https://github.com/NetApp/recline/workflows/build/badge.svg?branch=main)\n[![Gitter](https://badges.gitter.im/netapp-recline/community.svg)](https://gitter.im/netapp-recline/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)\n\n# recline\n\nWriting argparse-based command line applications can become tedious, repetitive,\nand difficult to do right. Relax and let this library free you from that burden.\n\nThis library helps you quickly implement an interactive command-based application in Python.\n\n## Documentation First\nWe all know that writing documentation is very important and yet it can easily become\nand afterthought or a nice to have if we\'re not diligent. This is often because it\nmeans duplicating a piece of your implementation in words, effectively writing the\nsame thing twice. Recline strives to deduplicate this work by taking a documentation\nfirst attitude where your documentation _becomes_ the implementation without additional\nwork from you.\n\n## Interactive\n\nThe default mode is to run a REPL interface where a prompt is given to the user, the\nuser types one of the available commands, the application processes it, displays the\nresult, and then control is returned to the user once more.\n\nBut if your user isn\'t expected to or doesn\'t always want to run multiple commands,\nyou also get a more traditional command-line interface for free.\n\n## Command-based\n\nThe application will be command based. Each command will have one or more words\nthat identify the command. It may also have one or more arguments that augment or\nvary the action that command will take.\n\n## Batteries included\n\nWhile the library is designed to be easy to implement for simple or small applications,\nit also comes with full power features for larger use cases including:\n\n* Tab completion\n* Input verification\n* Output formatting\n* Debugger integration\n\n# Before getting started\n\nSome things to consider and prepare before you can use this library.\n\n## Software requirements\n\n```\n1. Python 3.5 or later\n```\n\n## Installing and importing the library\n\nYou can install the package [from pypi](https://pypi.org/project/recline) using the pip utility:\n\n```\npip install recline\n```\n\nYou can then import the library into your application:\n\n```python\nimport recline\n```\n\n# Quick Start\n\nAfter installing the package, you can get started with a few lines in `hello.py`:\n\n```python\nimport recline\n\n@recline.command\ndef hello(name: str = None) -> None:\n    """A basic hello world\n\n    You can greet just about anybody with this command if they give you their name!\n\n    Args:\n        name: If a name is provided, the greeting will be more personal\n    """\n    response = "I\'m at your command"\n    if name:\n        response += ", %s" % name\n    print(response)\n\nrecline.relax()\n```\n\n## Interactive mode\n\nThe default mode when a recline applciation is run is an interactive style. Running\nour above `hello.py` results in the following output:\n\n```\n$ python hello.py\n> help\nAvailable Commands:\n\nhello - A basic hello world You can greet just about anybody with this command if\n\nBuilt-in Commands\n-----------------\nexit - Exit the application\nhelp - Display a list of available commands and their short description\nman - Display the full man page for a given command\n> hello ?\nA basic hello world You can greet just about anybody with this command if\n\nOptional arguments:\n  -name <name> If a name is provided, the greeting will be more personal\n    Default: None\n> hello\nI\'m at your command\n> hello -name Dave\nI\'m at your command, Dave\n> exit\n$\n```\n\n## Non-interactive mode\n\nIf you would like to use the application as part of a larger script, it is much\neasier to do in a non-interactive way. This is also possible using recline without\nneeding to change the application. Here\'s an example:\n\n```\n$ python hello.py -c "hello -name Dave"\nI\'m at your command, Dave\n$\n```\n\nSee the [full documentation](https://netapp.github.io/recline) for more advanced usages and examples\n\n# Contributing [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/NetApp/recline/issues)\n\nYou may read about the contribution process including how to build and test your changes [here](CONTRIBUTING.md).\n\n# Why recline?\n\nThere are a large number of different command line libraries on PyPi and GitHub.\nAnd some of them have the same sort of decorator design. Most, however, are missing\nthe interactive elements that recline focuses on (tab completion, command chaining,\nbackground jobs, man pages). If you\'re still looking for the right fit for your\napplication and recline isn\'t it, you can check out these other fine projects (in no\nparticular order):\n\n* https://github.com/kootenpv/cliche\n* https://github.com/gowithfloat/clippy\n* https://github.com/epsy/clize\n* https://github.com/pallets/click\n* https://github.com/micheles/plac\n* https://github.com/google/python-fire\n* https://github.com/kennethreitz-archive/clint\n* https://docs.openstack.org/cliff/latest\n* https://github.com/miguelgrinberg/climax\n',
    'author': 'NetApp',
    'author_email': 'ng-netapp-oss@netapp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NetApp/recline',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
