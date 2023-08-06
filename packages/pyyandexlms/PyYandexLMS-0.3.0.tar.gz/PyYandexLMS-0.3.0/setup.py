# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['PyYandexLMS',
 'PyYandexLMS.asynchronous',
 'PyYandexLMS.models',
 'PyYandexLMS.models.base',
 'PyYandexLMS.synchronous',
 'PyYandexLMS.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'pydantic>=1.9.1,<2.0.0', 'requests>=2.27.1,<3.0.0']

extras_require = \
{'docs': ['Sphinx>=4.2.0,<5.0.0',
          'sphinx-intl>=2.0.1,<3.0.0',
          'sphinx-autobuild>=2021.3.14,<2022.0.0',
          'sphinx-copybutton>=0.5.0,<0.6.0',
          'furo>=2022.4.7,<2023.0.0',
          'sphinx-prompt>=1.5.0,<2.0.0',
          'Sphinx-Substitution-Extensions>=2020.9.30,<2021.0.0',
          'towncrier>=21.9.0,<22.0.0',
          'pygments>=2.4,<3.0',
          'pymdown-extensions>=9.3,<10.0',
          'markdown-include>=0.6,<0.7',
          'Pygments>=2.11.2,<3.0.0',
          'm2r2>=0.3.2,<0.4.0']}

setup_kwargs = {
    'name': 'pyyandexlms',
    'version': '0.3.0',
    'description': '📡 Python API wrapper для LMS Яндекса с синхронными и асинхронными методами',
    'long_description': '<p align="center">\n    <a href="https://github.com/fast-geek/PyYandexLMS">\n        <img src="https://user-images.githubusercontent.com/67208948/170837642-d27a2d1c-8c18-443e-94c4-092904f705a7.png" alt="logo" height=150>\n    </a>\n    <br>\n    <b>Python API wrapper для LMS Яндекса с синхронными и асинхронными методами</b>\n    <br>\n    <a href="https://github.com/fast-geek/PyYandexLMS/tree/master/examples">\n        Examples\n    </a>\n    •\n    <a href="https://pypi.org/project/PyYandexLMS/">\n        PyPI\n    </a>\n</p>\n',
    'author': 'lav.',
    'author_email': 'me@lavn.ml',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fast-geek/PyYandexLMS',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
