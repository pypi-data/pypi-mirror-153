# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['user_email', 'user_email.migrations']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-user-email',
    'version': '1.0.4',
    'description': 'Custom, simple Django User model with email as username',
    'long_description': '<h1 align="center">\n  django-user-email\n</h1>\n\n<p align="center">\n  <a href="https://github.com/khasbilegt/django-user-email/">\n    <img src="https://img.shields.io/github/workflow/status/khasbilegt/django-user-email/test?label=CI&logo=github&style=for-the-badge" alt="ci status">\n  </a>\n  <a href="https://pypi.org/project/django-user-email/">\n    <img src="https://img.shields.io/pypi/v/django-user-email?style=for-the-badge" alt="pypi link">\n  </a>\n  <a href="https://codecov.io/github/khasbilegt/django-user-email">\n    <img src="https://img.shields.io/codecov/c/github/khasbilegt/django-user-email?logo=codecov&style=for-the-badge" alt="codecov">\n  </a>\n  <br>\n  <a>\n    <img src="https://img.shields.io/pypi/pyversions/django-user-email?logo=python&style=for-the-badge" alt="supported python versions">\n  </a>\n  <a>\n    <img src="https://img.shields.io/pypi/djversions/django-user-email?logo=django&style=for-the-badge" alt="supported django versions">\n  </a>\n</p>\n\n<p align="center">\n  <a href="#installation">Installation</a> •\n  <a href="#contributing">Contributing</a> •\n  <a href="#license">License</a>\n</p>\n\n<p align="center">Custom, simple Django User model with email as username</p>\n\n## Installation\n\n1. Use your preferred package manager ([pip](https://pip.pypa.io/en/stable/), [poetry](https://pypi.org/project/poetry/), [pipenv](https://pypi.org/project/pipenv/)) to install the package. For example:\n\n```bash\n$ poetry add django-user-email\n```\n\n2. Then register \'user_email\', in the \'INSTALLED_APPS\' section of your project\'s settings.\n\n```python\n# settings.py\n...\n\nINSTALLED_APPS = (\n    ...\n    \'user_email\',\n)\n\n...\n```\n\n3. Set AUTH_USER_MODEL - Since it\'s a custom User model Django needs to know the path of the model\n\n```bash\n# settings.py\n...\n\nAUTH_USER_MODEL = \'user_email.User\'\n\n...\n```\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT License](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Khasbilegt.TS',
    'author_email': 'khasbilegt.ts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khasbilegt/django-user-email',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
