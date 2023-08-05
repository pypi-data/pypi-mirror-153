# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['_primitives', 'primitives']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'primitives',
    'version': '1.8.0',
    'description': 'Fake objects designed with OOP in mind.',
    'long_description': '# Primitives [![build](https://img.shields.io/github/workflow/status/proofit404/primitives/release?style=flat-square)](https://github.com/proofit404/primitives/actions/workflows/release.yml?query=branch%3Arelease) [![pypi](https://img.shields.io/pypi/v/primitives?style=flat-square)](https://pypi.org/project/primitives)\n\nFake objects designed with OOP in mind.\n\n**[Documentation](https://proofit404.github.io/primitives) |\n[Source Code](https://github.com/proofit404/primitives) |\n[Task Tracker](https://github.com/proofit404/primitives/issues)**\n\nMock objects makes your tests worst. Usage of mock objects is considered an\nanti-pattern by many experienced developers. Mock objects blindly respond to any\ninteraction. Patch function is able to put such objects in any place in your\ncode. It does not matter if that code was written in a way to be configured or\nnot. This situation has several consequences.\n\nFirst of all, your tests start making assumptions about implementation of tested\ncode. This creates high coupling between tests and code. You no more could\neasily change your code because 25 tests are aware of the name of the function\nin the middle of the call stack.\n\nThe second unpleasant details about mocks is its fragile blind trust to the\nclient code. Writing mocks of proper quality is extremely complicated. You need\na ton of assert statements at the end of the test to check that only expected\nmethods were called. In addition API of the mock library in python is an ugly\nprocedural code. It requires a 3 lines just to define a dumb method returning\npredefined value on mock. This harms readability of tests dramatically.\n\nI was upset with mock library for the long time. I decided to design a\ncollection of strict composable objects without ability to put them at random\nplace in code. Here is what I came with!\n\n## Pros\n\n- Fake objects with strict behavior will highlight problems in your code earlier\n- Nice composable API makes definition of complex objects short and concrete\n- Force user to use composition instead of patch\n\n## Example\n\nThe `primitives` library gives you a collection of objects with ability to\ndefine expected behavior as set of short expressions. For example, you could\ndefine a function returning `None` like this:\n\n```pycon\n\n>>> from primitives import Instance, Callable, Argument\n\n>>> func = Callable()\n\n>>> func()\n\n```\n\nLet\'s try to test a function below using `primitives` fake objects and standard\n`unittest.mock` library for comparison.\n\n```pycon\n\n>>> def greet_many(repo):\n...    for user in repo.users():\n...        print(user.greet(\'Hello\'))\n\n>>> greet_many(Instance(users=Callable([\n...     Instance(greet=Callable(\'Hello, John\', Argument(\'Hello\'))),\n...     Instance(greet=Callable(\'Hello, Kate\', Argument(\'Hello\'))),\n... ])))\nHello, John\nHello, Kate\n\n```\n\nWe would leave `unittest.mock` implementation to the reader as a homework.\n\n## Questions\n\nIf you have any questions, feel free to create an issue in our\n[Task Tracker](https://github.com/proofit404/primitives/issues). We have the\n[question label](https://github.com/proofit404/primitives/issues?q=is%3Aopen+is%3Aissue+label%3Aquestion)\nexactly for this purpose.\n\n## Enterprise support\n\nIf you have an issue with any version of the library, you can apply for a paid\nenterprise support contract. This will guarantee you that no breaking changes\nwill happen to you. No matter how old version you\'re using at the moment. All\nnecessary features and bug fixes will be backported in a way that serves your\nneeds.\n\nPlease contact [proofit404@gmail.com](mailto:proofit404@gmail.com) if you\'re\ninterested in it.\n\n## License\n\n`primitives` library is offered under the two clause BSD license.\n\n<p align="center">&mdash; ⭐ &mdash;</p>\n',
    'author': 'Artem Malyshev',
    'author_email': 'proofit404@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/primitives',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
