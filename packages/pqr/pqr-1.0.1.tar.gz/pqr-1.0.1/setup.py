# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pqr']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'pqr',
    'version': '1.0.1',
    'description': 'Lightweight library for backtesting factor strategies',
    'long_description': '# pqr\n\npqr is a python library for backtesting factor strategies. It is built in top of numpy, so it is \nfast and memory efficient, but provides pandas interface to make usage more convenient and verbose.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install pqr.\n\n```bash\npip install pqr\n```\n\n## Quickstart\n\n```python\nimport pandas as pd\nimport pqr\n\nprices = pd.read_csv("prices.csv", parse_dates=True)\n\nmomentum = pqr.compose(\n    # picking\n    pqr.freeze(pqr.filter, universe=prices > 10),\n    pqr.freeze(pqr.look_back, period=12, agg="pct"),\n    pqr.freeze(pqr.lag, period=1),\n    pqr.freeze(pqr.hold, period=12),\n    pqr.freeze(pqr.quantiles, min_q=0.7, max_q=1),\n    # allocation\n    pqr.ew,\n    # evaluation\n    pqr.freeze(pqr.evaluate, universe_returns=pqr.to_returns(prices)),\n)\n\n# returns series of returns of 30% ew momentum 12-1-12 strategy for stocks > 10$\nmomentum(prices)\n```\n\n## Documentation\n\nThe official documentation is hosted on readthedocs.org: https://pqr.readthedocs.io/en/latest/\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would \nlike to change.\n\nPlease make sure to update tests and documentation as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Andrey Babkin',
    'author_email': 'andrey.babkin.ru71@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pqr.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
