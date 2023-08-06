# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['social_oauth_token', 'social_oauth_token.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django-oauth-toolkit>=1.5.0,<2.0.0', 'social-auth-app-django>=5.0.0,<6.0.0']

setup_kwargs = {
    'name': 'django-social-oauth-token',
    'version': '2.0.1',
    'description': 'OAuth Token generation API for handling OAuth 2.0 Authentication Code Flow based on social-auth',
    'long_description': '<h1 align="center">\n  django-social-oauth-token\n</h1>\n\n<p align="center">\n  <a href="https://github.com/khasbilegt/django-social-oauth-token/">\n    <img src="https://img.shields.io/github/workflow/status/khasbilegt/django-social-oauth-token/CI?label=CI&logo=github&style=for-the-badge" alt="ci status">\n  </a>\n  <a href="https://pypi.org/project/django-social-oauth-token/">\n    <img src="https://img.shields.io/pypi/v/django-social-oauth-token?style=for-the-badge" alt="pypi link">\n  </a>\n  <a href="https://codecov.io/github/khasbilegt/django-social-oauth-token">\n    <img src="https://img.shields.io/codecov/c/github/khasbilegt/django-social-oauth-token?logo=codecov&style=for-the-badge" alt="codecov">\n  </a>\n  <br>\n  <a>\n    <img src="https://img.shields.io/pypi/pyversions/django-social-oauth-token?logo=python&style=for-the-badge" alt="supported python versions">\n  </a>\n  <a>\n    <img src="https://img.shields.io/pypi/djversions/django-social-oauth-token?logo=django&style=for-the-badge" alt="supported django versions">\n  </a>\n</p>\n\n<p align="center">\n  <a href="#installation">Installation</a> •\n  <a href="#contributing">Contributing</a> •\n  <a href="#how-to-use">How To Use</a> •\n  <a href="#license">License</a>\n</p>\n\n<p align="center">OAuthToken generation API for handling OAuth 2.0 Authentication Code Flow based on social-auth</p>\n\n## Installation\n\n1. Use your preferred package manager ([pip](https://pip.pypa.io/en/stable/), [poetry](https://pypi.org/project/poetry/), [pipenv](https://pypi.org/project/pipenv/)) to install the package. For example:\n\n```bash\n$ poetry add django-social-oauth-token\n```\n\n2. Then register \'social_oauth_token\', in the \'INSTALLED_APPS\' section of your project\'s settings.\n\n```python\n# settings.py\n...\n\nINSTALLED_APPS = (\n    ...\n    \'social_oauth_token\',\n)\n\n...\n```\n\n3. Include the `urlpatterns` in your main `urls` file.\n\n```python\n# urls.py\n\nurlpatterns = [\n  ...\n  path("social_oauth_token/", include("social_oauth_token.urls", namespace="social_oauth_token")),\n  ...\n]\n\n```\n\n## How To Use\n\nIn order to verify the **Authorization Code** sent by the user and replace it with your own **OAuth Access Token**, send a **POST** request to the `token/<backend>/` endpoint with `client_id` and `code` to receive the token.\n\nThe POST request parameters:\n\n```Python\nclient_id # OAuth Client ID\ncode # Authorization Code\n```\n\nThe JSON response:\n\n```json\n{\n  "access_token": <access_token>,\n  "expires_in": <expires_in>,\n  "token_type": <token_type>,\n  "refresh_token": <refresh_token>,\n}\n```\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT License](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Khasbilegt.TS',
    'author_email': 'khasbilegt.ts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khasbilegt/django-social-oauth-token',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
