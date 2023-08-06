# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redshells',
 'redshells.app',
 'redshells.app.word_item_similarity',
 'redshells.contrib',
 'redshells.contrib.app',
 'redshells.contrib.app.word_item_similarity',
 'redshells.contrib.model',
 'redshells.contrib.train',
 'redshells.data',
 'redshells.factory',
 'redshells.model',
 'redshells.train',
 'redshells.train.utils']

package_data = \
{'': ['*']}

install_requires = \
['docutils==0.15',
 'gensim==3.8.3',
 'gokart>=0.1.20',
 'numpy',
 'optuna>=0.6.0',
 'pandas<1.2',
 'scikit-learn',
 'scipy',
 'tqdm']

setup_kwargs = {
    'name': 'redshells',
    'version': '0.1.22',
    'description': 'Tasks which are defined using gokart.TaskOnKart. The tasks can be used with data pipeline library "luigi".',
    'long_description': '# redshells\n\n[![Test](https://github.com/m3dev/redshells/actions/workflows/test.yml/badge.svg)](https://github.com/m3dev/redshells/actions/workflows/test.yml)\n[![Python Versions](https://img.shields.io/pypi/pyversions/redshells.svg)](https://pypi.org/project/redshells/)\n[![](https://img.shields.io/pypi/v/redshells)](https://pypi.org/project/redshells/)\n![](https://img.shields.io/pypi/l/redshells)\n\nMachine learning tasks which are used with data pipeline library "luigi" and its wrapper "gokart".\n\n## Dependencies\n\nYou should add `tensorflow = ">=1.13.1,<2.0"` on your app dependencies if you would like to use some models under `redshells/contrib` directory.\n`Tensorflow` is not included redshells\' dependencies because there are some models not used it.\n',
    'author': 'M3, inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m3dev/redshells',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
