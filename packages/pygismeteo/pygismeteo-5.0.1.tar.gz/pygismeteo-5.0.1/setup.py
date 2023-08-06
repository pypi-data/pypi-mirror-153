# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygismeteo']

package_data = \
{'': ['*']}

install_requires = \
['pygismeteo-base>=3.0,<4.0', 'requests>=2.27,<3.0']

setup_kwargs = {
    'name': 'pygismeteo',
    'version': '5.0.1',
    'description': 'Wrapper for Gismeteo API',
    'long_description': '# pygismeteo\n\n[![Build Status](https://github.com/monosans/pygismeteo/workflows/test/badge.svg?branch=main&event=push)](https://github.com/monosans/pygismeteo/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/monosans/pygismeteo/branch/main/graph/badge.svg)](https://codecov.io/gh/monosans/pygismeteo)\n\nОбёртка для [Gismeteo API](https://gismeteo.ru/api/).\n\nАсинхронная версия [здесь](https://github.com/monosans/aiopygismeteo).\n\n## Установка\n\n```bash\npython -m pip install -U pygismeteo\n```\n\n## Документация\n\n[pygismeteo.readthedocs.io](https://pygismeteo.readthedocs.io/)\n\n## Пример, выводящий температуру в Москве сейчас\n\n```python\nfrom pygismeteo import Gismeteo\n\ngm = Gismeteo()\nsearch_results = gm.search.by_query("Москва")\ncity_id = search_results[0].id\ncurrent = gm.current.by_id(city_id)\nprint(current.temperature.air.c)\n```\n\n## License / Лицензия\n\n[MIT](https://github.com/monosans/pygismeteo/blob/main/LICENSE)\n',
    'author': 'monosans',
    'author_email': 'hsyqixco@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/monosans/pygismeteo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
