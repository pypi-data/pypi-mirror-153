# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['eda_ja', 'eda_ja.resources', 'eda_ja.resources.stop_words']

package_data = \
{'': ['*']}

install_requires = \
['mecab-python3>=1.0.4,<2.0.0',
 'nltk>=3.6.5,<4.0.0',
 'pandas>=1.3.4,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'eda-ja',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Yuji Kamiya',
    'author_email': 'y.kamiya0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
