# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nba_bbref_webscrape']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==5.4.1',
 'SQLAlchemy>=1.4.37,<2.0.0',
 'awswrangler==2.14.0',
 'beautifulsoup4==4.9.3',
 'boto3==1.21.8',
 'html5lib==1.1',
 'lxml==4.8.0',
 'nltk>=3.7,<4.0',
 'pandas==1.3.5',
 'praw==7.5.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'requests==2.27.1',
 'sentry-sdk==1.5.8',
 'twint==2.1.20']

setup_kwargs = {
    'name': 'nba-bbref-webscrape',
    'version': '0.0.6',
    'description': 'Scraping basketball-reference.com w/ Pandas and BeautifulSoup4',
    'long_description': None,
    'author': 'jyablonski9',
    'author_email': 'jyablonski9@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jyablonski/nba_bbref_webscrape',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
