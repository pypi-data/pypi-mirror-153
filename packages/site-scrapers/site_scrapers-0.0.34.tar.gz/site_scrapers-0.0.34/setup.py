# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['site_scrapers',
 'site_scrapers.models',
 'site_scrapers.scrapers',
 'site_scrapers.scrapers.details',
 'site_scrapers.scrapers.list',
 'site_scrapers.tests',
 'site_scrapers.tests.scrapers',
 'site_scrapers.tests.scrapers.details',
 'site_scrapers.utils']

package_data = \
{'': ['*'],
 'site_scrapers.tests.scrapers.details': ['brc_data/*',
                                          'inchcape/*',
                                          'moller_data/*']}

install_requires = \
['gazpacho>=1.1,<2.0',
 'httpx>=0.23.0,<0.24.0',
 'requests>=2.27.1,<3.0.0',
 'returns>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'site-scrapers',
    'version': '0.0.34',
    'description': '',
    'long_description': '### Installation:\n\n`pip install site-scrapers`\n\n### What this does?\nWill fetch car details from dealership (concurrently)\n\n### Usage:\n\n```python\nimport asyncio\n\nfrom site_scrapers.scrapers import scrape_all\n\nif __name__ == \'__main__\':\n    results = asyncio.run(scrape_all())\n    print(*results, sep="\\n")  # will output fetched car details\n```\n\n### Supported Dealerships\nhttps://lietotiauto.mollerauto.lv  \nhttps://lv.brcauto.eu  \nhttps://certified.inchcape.lv/auto\n',
    'author': 'Dmitrijs Balcers,',
    'author_email': 'dmitrijs.balcers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dmitrijs-balcers/site_scrapers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
