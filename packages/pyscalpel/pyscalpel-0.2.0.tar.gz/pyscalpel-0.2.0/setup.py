# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scalpel',
 'scalpel.any_io',
 'scalpel.core',
 'scalpel.green',
 'scalpel.green.utils']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.0.0,<4.0.0',
 'attrs>=19.3.0,<20.0.0',
 'configuror>=0.2.0,<0.3.0',
 'fake-useragent>=0.1.11,<0.2.0',
 'httpx>=0.23.0,<0.24.0',
 'msgpack>=1.0.0,<2.0.0',
 'parsel>=1.5.2,<2.0.0',
 'rfc3986[idna]>=1.4.0,<2.0.0',
 'selenium>=3.141.0,<4.0.0']

extras_require = \
{'full': ['gevent>=20.9.0,<21.0.0', 'trio>=0.17.0,<0.18.0'],
 'gevent': ['gevent>=20.9.0,<21.0.0'],
 'trio': ['trio>=0.17.0,<0.18.0']}

setup_kwargs = {
    'name': 'pyscalpel',
    'version': '0.2.0',
    'description': 'Your easy-to-use, fast and powerful web scraping library',
    'long_description': '# Pyscalpel\n\n[![Pypi version](https://img.shields.io/pypi/v/pyscalpel.svg)](https://pypi.org/project/pyscalpel/)\n![](https://github.com/lewoudar/scalpel/workflows/CI/badge.svg)\n[![Coverage Status](https://codecov.io/gh/lewoudar/scalpel/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/gh/lewoudar/scalpel)\n[![Documentation Status](https://readthedocs.org/projects/scalpel/badge/?version=latest)](https://scalpel.readthedocs.io/en/latest/?badge=latest)\n[![License Apache 2](https://img.shields.io/hexpm/l/plug.svg)](http://www.apache.org/licenses/LICENSE-2.0)\n\nYour easy-to-use, fast and powerful web scraping library.\n\n## Why?\n\nI already knew [scrapy](https://docs.scrapy.org/en/latest/) which is the reference in python for web scraping. But\ntwo things bothered me.\n- I feel like scrapy cannot integrate into an existing project, you need to treat your web scraping stuff like a project\non its own.\n- Usage of [Twisted](https://twistedmatrix.com/trac/) who is a veteran in asynchronous programming, but I think\n that there are better asynchronous frameworks today. Note that this second point is not true anymore as I\'m writing\n the document since scrapy adds support for [asyncio](https://docs.scrapy.org/en/latest/topics/asyncio.html)\n \n After having made this observation I decided to create pyscalpel. And let\'s be honest, I also want to have my own web\n scraping library, and it is fun to write one ;)\n \n\n## Installation\n \n```bash\npip install pyscalpel  # to only use the asyncio backend\npip install pyscalpel[gevent] # to install the gevent backend\npip install pyscalpel[trio] # to installl the trio backend\npip install pyscalpel[full] # to install all the backends\n```\n\nIf you know about [poetry](https://python-poetry.org/) you can use it instead of pip.\n\n```bash\npoetry add pyscalpel  # to only use the asyncio backend\npoetry add pyscalpel[gevent] # to install the gevent backend\npoetry add pyscalpel[trio] # to install the trio backend\npoetry add pyscalpel[full] # to install all the backends\n```\n\npyscalpel works starting from **python 3.7**, it relies on robust packages:\n- [configuror](https://configuror.readthedocs.io/en/latest/): A configuration toolkit. \n- [httpx](https://www.python-httpx.org/): A modern http client.\n- [selenium](https://pypi.org/project/selenium/): A library for controlling a browser.\n- [gevent](http://www.gevent.org/): An asynchronous framework using the synchronous way. (optional)\n- [trio](https://trio.readthedocs.io/en/stable/): A modern asynchronous framework using `async/await` syntax. (optional)\n- [anyio](https://anyio.readthedocs.io/): An asynchronous networking and concurrency library that works on top of\neither asyncio or trio.\n- [parsel](https://parsel.readthedocs.io/): A library elements in HTML/XML documents.\n- [attrs](https://www.attrs.org/en/stable/): A library helping to write classes without pain.\n- [fake-useragent](https://pypi.org/project/fake-useragent/): A simple library to fake a user agent.\n- [rfc3986](https://rfc3986.readthedocs.io/en/latest/): A library for url parsing and validation.\n- [msgpack](https://pypi.org/project/msgpack/): A library allowing for fast serialization/deserialization of data\nstructures.\n\n## Documentation\n\nThe documentation is available at https://scalpel.readthedocs.io/en/latest/.\n\n\n## Usage\n\nTo give you an overview of what can be done, this is a simple example of quote scraping. Don\'t hesitate to look at the\nexamples folder for more snippets to look at.\n\nwith gevent\n\n```python\nfrom pathlib import Path\n\nfrom scalpel import Configuration\nfrom scalpel.green import StaticSpider, StaticResponse, read_mp\n\ndef parse(spider: StaticSpider, response: StaticResponse) -> None:\n    for quote in response.xpath(\'//div[@class="quote"]\'):\n        data = {\n            \'message\': quote.xpath(\'./span[@class="text"]/text()\').get(),\n            \'author\': quote.xpath(\'./span/small/text()\').get(),\n            \'tags\': quote.xpath(\'./div/a/text()\').getall()\n        }\n        spider.save_item(data)\n\n    next_link = response.xpath(\'//nav/ul/li[@class="next"]/a\').xpath(\'@href\').get()\n    if next_link is not None:\n        response.follow(next_link)\n\nif __name__ == \'__main__\':\n    backup = Path(__file__).parent / \'backup.mp\'\n    config = Configuration(backup_filename=f\'{backup}\')\n    spider = StaticSpider(urls=[\'http://quotes.toscrape.com\'], parse=parse, config=config)\n    spider.run()\n    print(spider.statistics())\n    # you can do whatever you want with the results\n    for quote_data in read_mp(filename=backup, decoder=spider.config.msgpack_decoder):\n        print(quote_data)\n```\n\nwith anyio\n\n```python\nfrom pathlib import Path\n\nimport anyio\nfrom scalpel import Configuration\nfrom scalpel.any_io import StaticResponse, StaticSpider, read_mp\n\n\nasync def parse(spider: StaticSpider, response: StaticResponse) -> None:\n    for quote in response.xpath(\'//div[@class="quote"]\'):\n        data = {\n            \'message\': quote.xpath(\'./span[@class="text"]/text()\').get(),\n            \'author\': quote.xpath(\'./span/small/text()\').get(),\n            \'tags\': quote.xpath(\'./div/a/text()\').getall()\n        }\n        await spider.save_item(data)\n\n    next_link = response.xpath(\'//nav/ul/li[@class="next"]/a\').xpath(\'@href\').get()\n    if next_link is not None:\n        await response.follow(next_link)\n\nasync def main():\n    backup = Path(__file__).parent / \'backup.mp\'\n    config = Configuration(backup_filename=f\'{backup}\')\n    spider = StaticSpider(urls=[\'http://quotes.toscrape.com\'], parse=parse, config=config)\n    await spider.run()\n    print(spider.statistics())\n    # you can do whatever you want with the results\n    async for item in read_mp(backup, decoder=spider.config.msgpack_decoder):\n        print(item)\n\nif __name__ == \'__main__\':\n    # by default, this will run the asyncio backend, if you want the trio backend, you must first install the trio \n    # package and replace the following line with: anyio.run(main, backend=\'trio\').\n    anyio.run(main)\n```\n\n## Known limitations\n\npyscalpel aims to handle SPA (single page application) through the use of selenium. However, due to the synchronous nature\nof selenium, it is hard to leverage anyio and gevent asynchronous feature. You will notice that the *selenium spider* is\nslower than the *static spider*. For more information look at the documentation.\n\n## Warning\n\npyscalpel is a young project, so it is expected to have breaking changes in the api without respecting the \n[semver](https://semver.org/) principle. It is recommended to pin the version you are using for now.',
    'author': 'lewoudar',
    'author_email': 'lewoudar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://scalpel.readthedocs.io/en/stable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
