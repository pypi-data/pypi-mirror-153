# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eztea',
 'eztea.django',
 'eztea.falcon',
 'eztea.sql',
 'eztea.sql.migration',
 'eztea.web']

package_data = \
{'': ['*'], 'eztea.sql.migration': ['template/*']}

install_requires = \
['ciso8601>=2.2.0', 'python-dotenv>=0.12.0', 'validr>=1.2.1']

extras_require = \
{'django': ['django>=4.0.3'],
 'falcon': ['falcon>=3.0.1',
            'sqlalchemy>=1.3.19',
            'sqlalchemy-jsonfield>=1.0.0',
            'sqlalchemy-utc>=0.14.0',
            'sqlalchemy-utils>=0.38.2'],
 'migration': ['click>=7.1.2',
               'alembic>=1.7.5',
               'black>=21.12b0',
               'mako>=1.1.6',
               'python-dateutil>=2.8.2'],
 'mysql': ['pymysql>=1.0.2', 'cryptography>=36.0.1,<37.0.0'],
 'postgresql': ['psycopg2>=2.9.3'],
 'testing': ['httpx>=0.22.0',
             'pytest>=6.2.5',
             'pytest-cov>=3.0.0',
             'pytest-env>=0.6.2',
             'coverage>=6.3.2']}

entry_points = \
{'console_scripts': ['eztea = eztea.__main__:main']}

setup_kwargs = {
    'name': 'eztea',
    'version': '0.1.10',
    'description': 'EZTea Web Framework',
    'long_description': '# EZTea Web Framework\n\n```bash\n# use falcon\npip install eztea[falcon,mysql,migration,testing]\n\n# use django\npip install eztea[django,postgresql,testing]\n```\n\n## Usage\n\n### Falcon Example\n\n```python\nfrom validr import T\n\nfrom eztea.falcon import Application, ResponderContext, Router\n\nrouter = Router()\n\n\n@router.get("/")\ndef hello(\n    ctx: ResponderContext,\n    name: str = T.str.default("world"),\n) -> T.dict(hello=T.str):\n    return {"hello": name}\n\n\napp = Application()\napp.include_router(router)\n```\n\n### Django Example\n\n```python\nfrom validr import T\n\nfrom django.http import HttpRequest\nfrom eztea.django import Router\n\nrouter = Router()\n\n\n@router.get("/")\ndef hello(\n    req: HttpRequest,\n    name: str = T.str.default("world"),\n) -> T.dict(hello=T.str):\n    return {"hello": name}\n\n\nurls = router.to_url_s()\n```\n\n### Testing Example\n\n```python\nfrom eztea.falcon.testing import WebTestClient\nfrom eztea.django.testing import WebTestClient\nfrom myapp.wsgi import application\n\ndef test_hello():\n    client = WebTestClient(application)\n    response = client.get(\'/\')\n    assert response.status_code == 200\n    assert reesponse.json() == {"hello": "world"}\n```\n',
    'author': 'guyskk',
    'author_email': 'guyskk@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guyskk/eztea',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9.7,<4.0',
}


setup(**setup_kwargs)
