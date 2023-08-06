# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['activesoup']

package_data = \
{'': ['*']}

install_requires = \
['html5lib>=0.9', 'requests>=2.9.0,<3.0.0', 'typing_extensions>=3.10,<4.0']

setup_kwargs = {
    'name': 'activesoup',
    'version': '0.3.1',
    'description': 'A pure-python headless browser',
    'long_description': 'activesoup\n==========\n\n.. image:: https://github.com/jelford/activesoup/workflows/Build/badge.svg\n    :target: https://github.com/jelford/activesoup/actions?query=workflow%3Abuild\n\n.. image:: https://img.shields.io/pypi/v/activesoup.svg?maxAge=3600\n    :target: https://pypi.python.org/pypi?:action=display&name=activesoup\n\nA simple library for interacting with the web from python\n\nDescription\n-----------\n\n``activesoup`` combines familiar python web capabilities for convenient\nheadless "browsing" functionality:\n\n* Modern HTTP support with `requests <https://docs.python-requests.org/>`__ -\n  connection pooling, sessions, ...\n* Convenient access to the web page with an interface inspired by\n  `beautifulsoup <https://www.crummy.com/software/BeautifulSoup/>`__ -\n  convenient HTML navigation.\n* Robust HTML parsing with\n  `html5lib <https://html5lib.readthedocs.org/en/latest/>`__ - parse the web\n  like browsers do.\n\nFull documentation can be found at https://activesoup.dev.\n\nUse cases\n---------\n\n``activesoup`` aims to provide just enough functionality for basic web automation\n/ crawler tasks. Consider using ``activesoup`` when:\n\n* You\'ve already checked out `requests-html <https://github.com/kennethreitz/requests-html>`__\n* You need to actively interact with some web-page from Python (e.g. submitting\n  forms, downloading files)\n* You don\'t control the site you need to interact with (if you do, just make an\n  API).\n* You don\'t need javascript support (you\'ll need\n  `selenium <http://www.seleniumhq.org/projects/webdriver/>`__ or\n  `phantomjs <http://phantomjs.org/>`__).\n\nUsage examples\n--------------\n\nIn the example below, we\'ll load a page with a simple form, enumerate\nthe fields, and make a submission:\n\n.. code-block:: python\n\n    >>> import activesoup\n\n    >>> # Start a session\n    >>> d = activesoup.Driver()\n\n    >>> page = d.get("https://httpbin.org/forms/post")\n\n    >>> # conveniently access elements, inspired by BeautifulSoup\n    >>> form = page.form\n\n    >>> # get the power of raw xpath search too\n    >>> form.find(\'.//input[@name="size"]\')\n    BoundTag<input>\n    >>> # any element, searching by attribute\n    >>> form.find(\'.//*\', name="size")\n    BoundTag<input>\n    >>> # or just search by attribute\n    >>> form.find(name="size")\n    BoundTag<input>\n\n    >>> # inspect element attributes\n    >>> print([i[\'name\'] for i in form.find_all(\'input\')])\n    [\'custname\', \'custtel\', \'custemail\', \'size\', \'size\', \'size\', \'topping\', \'topping\', \'topping\', \'topping\', \'delivery\']\n\n    >>> # work actively with objects on the page\n    >>> r = form.submit({"custname": "john", "size": "small"})\n\n    >>> # responses parsed and ready based on content type\n    >>> r.keys()\n    dict_keys([\'args\', \'data\', \'files\', \'form\', \'headers\', \'json\', \'origin\', \'url\'])\n    >>> r[\'form\']\n    {\'custname\': \'john\', \'size\': \'small\', \'topping\': \'mushroom\'}\n\n    >>> # access the underlying requests.Session too\n    >>> d.session\n    <requests.sessions.Session object at 0x7f283dc95700>\n\n    >>> # log in with cookie support\n    >>> d.get(\'https://httpbin.org/cookies/set/foo/bar\')\n    >>> d.session.cookies[\'foo\']\n    \'bar\'\n',
    'author': 'James Elford',
    'author_email': 'james.p.elford@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jelford/activesoup',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.7,<4.0.0',
}


setup(**setup_kwargs)
