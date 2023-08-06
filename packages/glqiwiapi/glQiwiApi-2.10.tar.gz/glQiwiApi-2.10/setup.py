# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glQiwiApi',
 'glQiwiApi.contrib',
 'glQiwiApi.core',
 'glQiwiApi.core.abc',
 'glQiwiApi.core.cache',
 'glQiwiApi.core.event_fetching',
 'glQiwiApi.core.event_fetching.class_based',
 'glQiwiApi.core.event_fetching.webhooks',
 'glQiwiApi.core.event_fetching.webhooks.dto',
 'glQiwiApi.core.event_fetching.webhooks.middlewares',
 'glQiwiApi.core.event_fetching.webhooks.services',
 'glQiwiApi.core.event_fetching.webhooks.services.security',
 'glQiwiApi.core.event_fetching.webhooks.views',
 'glQiwiApi.core.session',
 'glQiwiApi.ext',
 'glQiwiApi.plugins',
 'glQiwiApi.plugins.aiogram',
 'glQiwiApi.qiwi',
 'glQiwiApi.qiwi.clients',
 'glQiwiApi.qiwi.clients.maps',
 'glQiwiApi.qiwi.clients.maps.methods',
 'glQiwiApi.qiwi.clients.maps.types',
 'glQiwiApi.qiwi.clients.p2p',
 'glQiwiApi.qiwi.clients.p2p.methods',
 'glQiwiApi.qiwi.clients.wallet',
 'glQiwiApi.qiwi.clients.wallet.methods',
 'glQiwiApi.qiwi.clients.wallet.methods.qiwi_master',
 'glQiwiApi.qiwi.clients.wallet.methods.webhook',
 'glQiwiApi.qiwi.clients.wallet.types',
 'glQiwiApi.types',
 'glQiwiApi.types.arbitrary',
 'glQiwiApi.utils',
 'glQiwiApi.utils.synchronous',
 'glQiwiApi.yoo_money',
 'glQiwiApi.yoo_money.methods',
 'glQiwiApi.yoo_money.types']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.0,<4.0.0', 'pydantic>=1.9.0,<2.0.0', 'pytz==2022.1']

extras_require = \
{':python_version <= "3.7"': ['typing_extensions>=4.0.1,<5.0.0'],
 'docs': ['Sphinx>=4.2.0,<5.0.0',
          'sphinx-intl>=2.0.1,<3.0.0',
          'sphinx-autobuild>=2021.3.14,<2022.0.0',
          'sphinx-copybutton>=0.5.0,<0.6.0',
          'furo>=2022.2.23,<2023.0.0',
          'sphinx-prompt>=1.5.0,<2.0.0',
          'Sphinx-Substitution-Extensions>=2020.9.30,<2021.0.0',
          'towncrier>=21.3.0,<22.0.0',
          'pygments>=2.4,<3.0',
          'pymdown-extensions>=9.4,<10.0',
          'markdown-include>=0.6,<0.7',
          'sphinxemoji',
          'sphinx-notfound-page'],
 'fast': ['aiofiles>=0.8.0,<0.9.0'],
 'fast:sys_platform == "darwin" or sys_platform == "linux"': ['uvloop>=0.16.0,<0.17.0']}

setup_kwargs = {
    'name': 'glqiwiapi',
    'version': '2.10',
    'description': 'The ultrarapid and multifunctional wrapper over QIWI and YooMoney',
    'long_description': '<h2 align="center">\n<img src="https://github.com/GLEF1X/glQiwiApi/blob/dev-2.x/docs/_static/logo.png?raw=true" width="200"></img>\n\n\n[![PyPI version](https://img.shields.io/pypi/v/glQiwiApi.svg)](https://pypi.org/project/glQiwiApi/) [![Code Quality Score](https://api.codiga.io/project/20780/score/svg)](https://frontend.code-inspector.com/public/project/20780/glQiwiApi/dashboard) ![Downloads](https://img.shields.io/pypi/dm/glQiwiApi) ![docs](https://readthedocs.org/projects/pip/badge/?version=latest)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/GLEF1X/glQiwiApi.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/GLEF1X/glQiwiApi/context:python) [![CodeFactor](https://www.codefactor.io/repository/github/glef1x/glqiwiapi/badge)](https://www.codefactor.io/repository/github/glef1x/glqiwiapi)\n![codecov](https://codecov.io/gh/GLEF1X/glQiwiApi/branch/dev-2.x/graph/badge.svg?token=OD538HKV15)\n![CI](https://github.com/GLEF1X/glQiwiApi/actions/workflows/tests.yml/badge.svg) ![mypy](https://img.shields.io/badge/%20type_checker-mypy-%231674b1?style=flat) [![Downloads](https://pepy.tech/badge/glqiwiapi/month)](https://pepy.tech/project/glqiwiapi) [![Downloads](https://pepy.tech/badge/glqiwiapi)](https://pepy.tech/project/glqiwiapi)\n\n<img src="https://github.com/GLEF1X/glQiwiApi/blob/dev-2.x/demo.gif"/>\n</h2>\n\n**glQiwiApi 2.x has breaking changes** \n\n## 🌎Official api resources:\n\n* 🎓 __Documentation: [here](https://glqiwiapi.readthedocs.io/en/latest/)__\n* 🖱️ __Telegram chat: [![Dev-Telegram](https://img.shields.io/badge/Telegram-blue.svg?style=flat-square&logo=telegram)](https://t.me/glQiwiAPIOfficial)__\n\n## Benchmarks\n\n```bash\nhint: smaller is better\nglQiwiApi      90.9925 (1.0)      103.3993 (1.0)       95.4082 (1.0)      5.3941 (1.0)       92.4023 (1.0)       8.2798 (1.0)\npyQiwiP2P     112.2819 (1.23)     135.0227 (1.31)     123.7498 (1.30)     9.9919 (1.85)     127.5926 (1.38)     17.2723 (2.09) \n```\n\n## 🐦Dependencies\n\n| Library |                       Description                       |\n|:-------:|:-------------------------------------------------------:|\n|aiohttp  | Asynchronous HTTP Client/Server for asyncio and Python. |\n|pydantic |    Json data validator. Very fast instead of custom     |\n',
    'author': 'Glib Garanin',
    'author_email': 'glebgar567@gmail.com',
    'maintainer': 'GLEF1X',
    'maintainer_email': 'glebgar567@gmail.com',
    'url': 'https://github.com/GLEF1X/glQiwiApi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
