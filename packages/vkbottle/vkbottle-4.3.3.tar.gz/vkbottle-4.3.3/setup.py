# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vkbottle',
 'vkbottle.api',
 'vkbottle.api.request_rescheduler',
 'vkbottle.api.request_validator',
 'vkbottle.api.response_validator',
 'vkbottle.api.token_generator',
 'vkbottle.callback',
 'vkbottle.dispatch',
 'vkbottle.dispatch.dispenser',
 'vkbottle.dispatch.handlers',
 'vkbottle.dispatch.middlewares',
 'vkbottle.dispatch.return_manager',
 'vkbottle.dispatch.return_manager.bot',
 'vkbottle.dispatch.return_manager.user',
 'vkbottle.dispatch.rules',
 'vkbottle.dispatch.views',
 'vkbottle.dispatch.views.abc',
 'vkbottle.dispatch.views.bot',
 'vkbottle.dispatch.views.user',
 'vkbottle.exception_factory',
 'vkbottle.exception_factory.error_handler',
 'vkbottle.exception_factory.swear_handler',
 'vkbottle.framework',
 'vkbottle.framework.bot',
 'vkbottle.framework.labeler',
 'vkbottle.framework.user',
 'vkbottle.http',
 'vkbottle.polling',
 'vkbottle.tools',
 'vkbottle.tools.dev',
 'vkbottle.tools.dev.keyboard',
 'vkbottle.tools.dev.mini_types',
 'vkbottle.tools.dev.mini_types.base',
 'vkbottle.tools.dev.mini_types.bot',
 'vkbottle.tools.dev.mini_types.user',
 'vkbottle.tools.dev.storage',
 'vkbottle.tools.dev.template',
 'vkbottle.tools.dev.uploader',
 'vkbottle.tools.dev.vkscript_converter',
 'vkbottle.tools.production',
 'vkbottle.tools.production.legacies']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'aiohttp>=3.6.2,<4.0.0',
 'choicelib>=0.1.5,<0.2.0',
 'pydantic>=1.8.2,<2.0.0',
 'typing-extensions>=4.0.1,<5.0.0',
 'vbml>=1.1.post1,<2.0',
 'vkbottle-types>=5.131.146.3,<6.0.0.0',
 'watchgod>=0.7,<0.9']

setup_kwargs = {
    'name': 'vkbottle',
    'version': '4.3.3',
    'description': 'Homogenic! Customizable asynchronous VK API framework implementing comfort and speed',
    'long_description': '<p align="center">\n  <a href="https://github.com/vkbottle/vkbottle">\n    <img src="https://raw.githubusercontent.com/vkbottle/vkbottle/master/docs/logo.svg" width="175px" style="display: inline-block; border-radius: 5px">\n  </a>\n</p>\n<h1 align="center">\n  VKBottle 4.x\n</h1>\n<p align="center">\n  <img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/vkbottle/vkbottle/CI?style=flat-square">\n  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/vkbottle/vkbottle?style=flat-square">\n  <img alt="GitHub issues by-label" src="https://img.shields.io/github/issues/vkbottle/vkbottle/bug?style=flat-square">\n  <img alt="PyPI" src="https://img.shields.io/pypi/v/vkbottle?color=green&label=PyPI&style=flat-square">\n</p>\n\n> Кастомизируемый, быстрый и удобный фреймворк для работы с VK API\n\n## Документация\n\n[Туториал для новичков](https://vkbottle.readthedocs.io/ru/latest/tutorial/)\\\n[Техническая документация](https://vkbottle.readthedocs.io/ru/latest)\n\n## Установка\n\nУстановить новейшую версию можно командой:\n\n```shell\npip install -U https://github.com/vkbottle/vkbottle/archive/master.zip\n```\n\nУстановить последнюю версию VKBottle 4.x с PyPI можно командой:\n\n```shell\npip install vkbottle\n```\n\nЕсли вы ищете старые версии:\n- [`3.x`](https://github.com/vkbottle/vkbottle/tree/v3.0)\n- [`2.x`](https://github.com/vkbottle/vkbottle/tree/v2.0)\n\n## Hello World\n\n[Смотреть больше примеров!](https://github.com/vkbottle/vkbottle/tree/master/examples)\\\n[Почему VKBottle?](https://github.com/vkbottle/vkbottle/blob/master/docs/why_vkbottle.md)\n\n```python\nfrom vkbottle.bot import Bot\n\nbot = Bot("GroupToken")\n\n@bot.on.message()\nasync def handler(_) -> str:\n    return "Hello world!"\n\nbot.run_forever()\n```\n\n## Contributing\n\nПР поддерживаются! Перед созданием пулл реквеста ознакомьтесь с [CONTRIBUTION_GUIDE.md](CONTRIBUTION_GUIDE.md). Нам приятно видеть ваш вклад в развитие библиотеки. Задавайте вопросы в блоке Issues и в [**чате Telegram**](https://t.me/vkbottle_ru) / [**чате VK**](https://vk.me/join/AJQ1d7fBUBM_800lhEe_AwJj)!\n\n* Создатель [@timoniq](https://github.com/timoniq)\n* Мейнтейнер [@FeeeeK](https://github.com/FeeeeK)\n\n## Лицензия\n\nCopyright © 2019-2021 [timoniq](https://github.com/timoniq).\\\nCopyright © 2022 [FeeeeK](https://github.com/FeeeeK).\\\nЭтот проект имеет [MIT](https://github.com/vkbottle/vkbottle/blob/master/LICENSE) лицензию.\n',
    'author': 'timoniq',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vkbottle/vkbottle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
