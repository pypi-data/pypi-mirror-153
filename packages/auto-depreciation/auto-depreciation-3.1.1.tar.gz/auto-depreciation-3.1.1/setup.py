# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auto_depreciation']

package_data = \
{'': ['*']}

install_requires = \
['beancount>=2.3.5,<3.0.0', 'python-dateutil>=2.8.2,<3.0.0']

extras_require = \
{'docs': ['mike>=1.1.2,<2.0.0',
          'mkdocs>=1.2.3,<2.0.0',
          'mkdocs-material>=8.2.1,<9.0.0'],
 'test': ['pytest>=7.1.2,<8.0.0', 'pytest-cov>=3.0.0,<4.0.0']}

setup_kwargs = {
    'name': 'auto-depreciation',
    'version': '3.1.1',
    'description': 'Beancount plugin for fixed assets depreciation',
    'long_description': '# Auto Depreciation Plugin\n\n[Auto depreciation](https://hktkzyx.github.io/auto-depreciation/)\nis a [beancount](https://github.com/beancount/beancount) plugin to deal with fixed assets depreciation.\nIn our daily life, we may buy some valuable goods like cars, phones, furniture, etc.\nAll these transactions are preferred to be documented as transfer instead of expenses,\notherwise, you cannot evaluate your daily expenses properly.\nThis plugin can generate depreciation transactions automatically.\n\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/hktkzyx/auto-depreciation/build-and-test)](https://github.com/hktkzyx/auto-depreciation/actions)\n[![Codecov](https://img.shields.io/codecov/c/github/hktkzyx/auto-depreciation)](https://app.codecov.io/gh/hktkzyx/auto-depreciation)\n[![PyPI](https://img.shields.io/pypi/v/auto-depreciation)](https://pypi.org/project/auto-depreciation/)\n[![PyPI - License](https://img.shields.io/pypi/l/auto-depreciation)](https://github.com/hktkzyx/auto-depreciation/blob/master/LICENSE)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/auto-depreciation)](https://pypi.org/project/auto-depreciation/)\n[![GitHub last commit](https://img.shields.io/github/last-commit/hktkzyx/auto-depreciation)](https://github.com/hktkzyx/auto-depreciation)\n\n## Installing\n\n```bash\npip install auto-depreciation\n```\n\n## Configuration\n\nThe parameters passed to the plugin are:\n\n- `assets`: Fixed assets account.\n- `expenses`: Depreciation expenses account.\n- `method`: Depreciation method.\n\nParameter default values are as follows:\n\n```\nplugin "auto_depreciation.depreciation" "{\n    \'assets\':\'Assets:Wealth:Fixed-Assets\',\n    \'expenses\':\'Expenses:Property-Expenses:Depreciation\',\n    \'method\':\'parabola\',\n}"\n```\n\n## Usage\n\nXiaoming is a young man. One day he bought a car and paid in cash.\nWe assume that the original value of that car is 100,000 CNY\nand it will scrap after 10 years.\nThe residual value is still 1,000 CNY.\n\nHe can use this plugin like this:\n\n!!! example\n\n    ```\n    plugin "auto_depreciation.depreciation"\n\n    2020-03-01 commodity CARS\n        name: "cars"\n        assets-class: "fixed assets"\n\n    2020-03-31 * ""\n        Assets:Cash                     -100000.00 CNY\n        Assets:Wealth:Fixed-Assets           1 CARS {100000.00 CNY, "BMW"}\n            useful_life: "10y"\n            residual_value: 1000\n    ```\n\nwhere we use metadata attached in the posting to pass residual value and useful life to plugin.\n\n`useful_life` is the compulsory item and `y` represent *years* while `m` represent *months*.\n\n`residual_value` is optional and by default 0.\n\n!!! note\n\n    `residual_value` is rounded to 2 decimal places.\n\n!!! example\n\n    ```\n    2020-03-31 * "Example"\n        Assets:Cash              -600.00 CNY\n        Assets:Wealth:Fixed-Assets        1 LENS {600.00 CNY, "Nikon"}\n            useful_life: "3m"\n            residual_value: 200\n    ```\n\n    The code above is equal to\n\n    ```\n    2020-03-31 * "Example"\n        Assets:Cash                     -600.00 CNY\n        Assets:Wealth:Fixed-Assets        1 LENS {600.00 CNY, 2020-03-31, "Nikon"}\n            useful_life: "3m"\n            residual_value: 200\n\n    2020-04-30 * "Example-auto_depreciation:Nikon"\n        Assets:Wealth:Fixed-Assets              -1 LENS {600.00 CNY, 2020-03-31, "Nikon"}\n        Assets:Wealth:Fixed-Assets               1 LENS {379.74 CNY, 2020-04-30, "Nikon"}\n        Expenses:Property-Expenses:Depreciation    220.26 CNY\n\n    2020-05-31 * "Example-auto_depreciation:Nikon"\n        Assets:Wealth:Fixed-Assets              -1 LENS {379.74 CNY, 2020-04-30, "Nikon"}\n        Assets:Wealth:Fixed-Assets               1 LENS {243.47 CNY, 2020-05-31, "Nikon"}\n        Expenses:Property-Expenses:Depreciation    136.27 CNY\n\n    2020-06-30 * "Example-auto_depreciation:Nikon"\n        Assets:Wealth:Fixed-Assets              -1 LENS {243.47 CNY, 2020-05-31, "Nikon"}\n        Assets:Wealth:Fixed-Assets               1 LENS {200 CNY, 2020-06-30, "Nikon"}\n        Expenses:Property-Expenses:Depreciation     43.47 CNY\n    ```\n\nIf the amount of fixed assets is greater than 1, all will be depreciated like this:\n\n!!! example\n\n    ```\n    2020-03-31 * "Example"\n        Assets:Cash                    -1200.00 CNY\n        Assets:Wealth:Fixed-Assets        2 LENS {600.00 CNY, 2020-03-31, "Nikon"}\n            useful_life: "3m"\n            residual_value: 200\n\n    2020-04-30 * "Example-auto_depreciation:Nikon"\n        Assets:Wealth:Fixed-Assets              -2 LENS {600.00 CNY, 2020-03-31, "Nikon"}\n        Assets:Wealth:Fixed-Assets               2 LENS {379.74 CNY, 2020-04-30, "Nikon"}\n        Expenses:Property-Expenses:Depreciation    440.52 CNY\n\n    ...\n    ```\n',
    'author': 'Brooks YUAN',
    'author_email': 'hktkzyx@yeah.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hktkzyx.github.io/auto-depreciation/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
