# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_rss_reader']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.7,<4.0']

setup_kwargs = {
    'name': 'yet-another-simple-rss-parser',
    'version': '0.0.5',
    'description': 'Simple RSS reader/parser',
    'long_description': '# simple_rss_reader\n\nAs an happy customer of Alfred 4 APP, i was in a need for simplest RSS parser.\nI decided to write the simplest one for my needs. \n\nThen i said to myself, why not to make it open source as a package for anyone who need it. \nAlthough its 2022, and XML should be an no more then  (not so great) history, i know that if i need it, i can only assume i am not the only one. \n\nFeel free to use, fork, and learn (although it is as minimal and simple as possible)\n\n\n## INSTALL\nrun: \n```\npip install  yet-another-simple-rss-parser\n```\n\n## Usage\n\n```\n\nfrom simple_rss_reader.reader import SimpleRssReader\n\n\nr = SimpleRssReader(url) # url of source or xml string\n\n# load as dict\nv = r.to_dict()\n\n#  get as json\nv = r.to_json()\n\n# get list of items (without header)\nv = r.get_tiems()\n```\n\nThe package homepage in pypi: https://www.pypi.org/project/yet-another-simple-rss-parser/\nSource code is hosted in github: https://github.com/barakbl/simple_rss_reader\n',
    'author': 'Barak Bloch',
    'author_email': 'barak.bloch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.pypi.org/project/yet-another-simple-rss-parser/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
