# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['some_models']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.33,<2.0.0', 'psycopg2>=2.9,<3.0']

setup_kwargs = {
    'name': 'some-models',
    'version': '0.3.0',
    'description': 'Учебная библиотека. Тут находятся orm модели нужные в нескольких микросервисах, что бы не нарушать DRY.',
    'long_description': 'None',
    'author': 'koevgeny10',
    'author_email': 'koevgeny10@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
