# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiopygismeteo']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8,<4.0', 'pygismeteo-base>=3.0,<4.0']

setup_kwargs = {
    'name': 'aiopygismeteo',
    'version': '5.0.0',
    'description': 'Asynchronous wrapper for Gismeteo API',
    'long_description': '# aiopygismeteo\n\n[![Build Status](https://github.com/monosans/aiopygismeteo/workflows/test/badge.svg?branch=main&event=push)](https://github.com/monosans/aiopygismeteo/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/monosans/aiopygismeteo/branch/main/graph/badge.svg)](https://codecov.io/gh/monosans/aiopygismeteo)\n\nАсинхронная обёртка для [Gismeteo API](https://gismeteo.ru/api/).\n\nСинхронная версия [здесь](https://github.com/monosans/pygismeteo).\n\n## Установка\n\n```bash\npython -m pip install -U aiopygismeteo\n```\n\n## Документация\n\n<https://aiopygismeteo.readthedocs.io/>\n\n## Пример, выводящий температуру в Москве сейчас\n\n```python\nimport asyncio\n\nfrom aiopygismeteo import Gismeteo\n\n\nasync def main():\n    gm = Gismeteo()\n    search_results = await gm.search.by_query("Москва")\n    city_id = search_results[0].id\n    current = await gm.current.by_id(city_id)\n    print(current.temperature.air.c)\n\n\nasyncio.run(main())\n```\n\n## License / Лицензия\n\n[MIT](https://github.com/monosans/aiopygismeteo/blob/main/LICENSE)\n',
    'author': 'monosans',
    'author_email': 'hsyqixco@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/monosans/aiopygismeteo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
