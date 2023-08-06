# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['listparser']

package_data = \
{'': ['*']}

extras_require = \
{'http': ['requests>=2.25.1,<3.0.0'], 'lxml': ['lxml>=4.6.2,<5.0.0']}

setup_kwargs = {
    'name': 'listparser',
    'version': '0.19',
    'description': 'Parse OPML subscription lists',
    'long_description': 'listparser\n==========\n\n*Parse OPML subscription lists in Python.*\n\n-------------------------------------------------------------------------------\n\nIf you\'re building a feed reader and you need to parse OPML subscription lists,\nyou\'ve come to the right place!\n\nlistparser makes it easy to parse and use subscription lists in multiple formats.\nIt supports OPML, RDF+FOAF, and the iGoogle exported settings format,\nand runs on Python 3.7+ and on PyPy 3.7.\n\n\n\nUsage\n=====\n\n..  code-block:: pycon\n\n    >>> import listparser\n    >>> result = listparser.parse(open(\'feeds.opml\').read())\n\nA dictionary will be returned with several keys:\n\n*   ``meta``: a dictionary of information about the subscription list\n*   ``feeds``: a list of feeds\n*   ``lists``: a list of subscription lists\n*   ``version``: a format identifier like "opml2"\n*   ``bozo``: True if there is a problem with the list, False otherwise\n*   ``bozo_exception``: (if ``bozo`` is 1) a description of the problem\n\nFor convenience, the result dictionary supports attribute access for its keys.\n\nContinuing the example:\n\n..  code-block:: pycon\n\n    >>> result.meta.title\n    \'listparser project feeds\'\n    >>> len(result.feeds)\n    2\n    >>> result.feeds[0].title, result.feeds[0].url\n    (\'listparser blog\', \'https://kurtmckee.org/tag/listparser\')\n\nMore extensive documentation is available in the ``docs/`` directory\nand online at <https://listparser.readthedocs.io/en/stable/>.\n\n\nBugs\n====\n\nThere are going to be bugs. The best way to handle them will be to\nisolate the simplest possible document that susses out the bug, add\nthat document as a test case, and then find and fix the problem.\n\n...you can also just report the bug and leave it to someone else\nto fix the problem, but that won\'t be as much fun for you!\n\nBugs can be reported at <https://github.com/kurtmckee/listparser/issues>.\n',
    'author': 'Kurt McKee',
    'author_email': 'contactme@kurtmckee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kurtmckee/listparser/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
