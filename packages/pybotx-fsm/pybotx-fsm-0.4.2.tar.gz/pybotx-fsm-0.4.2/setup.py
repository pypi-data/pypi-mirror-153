# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybotx_fsm']

package_data = \
{'': ['*']}

install_requires = \
['pybotx>=0.35.0,<0.45.0']

setup_kwargs = {
    'name': 'pybotx-fsm',
    'version': '0.4.2',
    'description': 'FSM middleware for using with pybotx',
    'long_description': '# pybotx-fsm\n\n[![codecov](https://codecov.io/gh/ExpressApp/pybotx-fsm/branch/master/graph/badge.svg?token=JWT9JWU2Z4)](https://codecov.io/gh/ExpressApp/pybotx-fsm)\n\nКонечный автомат (Finite state machine) для ботов на базе библиотеки\n[pybotx](https://github.com/ExpressApp/pybotx).\n\n\n## Возможности\n\n* Лёгкое создание графа состояний и их переключений.\n* Передача данных в следующее состояние при явном вызове перехода.\n\n\n## Подготовка к установке\n\nДля работы библиотеки необходим Redis, который уже встроен в последние версии\n[коробки](https://github.com/ExpressApp/async-box).\n\n\n## Установка\nИспользуя `poetry`:\n\n```bash\npoetry add pybotx-fsm\n```\n\n## Работа с графом состояний\n\n1. Создайте `enum` для возможных состояний автомата:\n\n```python #fsm_init\nfrom enum import Enum, auto\n\nfrom pybotx_fsm import FSMCollector\n\n\nclass LoginStates(Enum):\n    enter_email = auto()\n    enter_password = auto()\n\n\nfsm = FSMCollector(LoginStates)\n```\n\n\n2. Добавьте экземпляр автомата в мидлвари для того, чтобы бот мог использовать его:\n\n```python #fsm_usage\nBot(\n    collectors=[\n        myfile.collector,\n    ],\n    bot_accounts=[\n        BotAccountWithSecret(\n            # Не забудьте заменить эти учётные данные на настоящие,\n            # когда создадите бота в панели администратора.\n            id=UUID("123e4567-e89b-12d3-a456-426655440000"),\n            host="cts.example.com",\n            secret_key="e29b417773f2feab9dac143ee3da20c5",\n        ),\n    ],\n    middlewares=[\n        FSMMiddleware([myfile.fsm], state_repo_key="redis_repo"),\n    ],\n)\n```\n\n3. Добавьте в `bot.state.{state_repo_key}` совместимый redis репозиторий:\n\n```python #noqa\nbot.state.redis_repo = await RedisRepo.init(...)\n```\n\n\n4. Создайте обработчики конкретных состояний:\n\n```python #fsm_state_handlers\n@fsm.on(LoginStates.enter_email)\nasync def enter_email(message: IncomingMessage, bot: Bot) -> None:\n    email = message.body\n\n    if not check_user_exist(email):\n        await bot.answer_message("Wrong email, try again")\n        return\n\n    await message.state.fsm.change_state(LoginStates.enter_password, email=email)\n    await bot.answer_message("Enter your password")\n\n\n@fsm.on(LoginStates.enter_password)\nasync def enter_password(message: IncomingMessage, bot: Bot) -> None:\n    email = message.state.fsm_storage.email\n    password = message.body\n\n    try:\n        login(email, password)\n    except IncorrectPasswordError:\n        await bot.answer_message("Wrong password, try again")\n        return\n\n    await message.state.fsm.drop_state()\n    await bot.answer_message("Success!")\n```\n\n5. Передайте управление обработчику состояний из любого обработчика сообщений:\n\n```python #fsm_change_state\n@collector.command("/login")\nasync def start_login(message: IncomingMessage, bot: Bot) -> None:\n    await bot.answer_message("Enter your email")\n    await message.state.fsm.change_state(LoginStates.enter_email)\n```\n\n\n## Примеры\n\n### Минимальный пример бота с конечным автоматом\n\n```python #fsm_sample\n# Здесь и далее будут пропущены импорты и код, не затрагивающий\n# непосредственно pybotx_fsm\nclass FsmStates(Enum):\n    EXAMPLE_STATE = auto()\n\n\nfsm = FSMCollector(FsmStates)\n\n\n@collector.command("/echo", description="Echo command")\nasync def help_command(message: IncomingMessage, bot: Bot) -> None:\n    await message.state.fsm.change_state(FsmStates.EXAMPLE_STATE)\n    await bot.answer_message("Input your text:")\n\n\n@fsm.on(FsmStates.EXAMPLE_STATE)\nasync def example_state(message: IncomingMessage, bot: Bot) -> None:\n    user_text = message.body\n    await message.state.fsm.drop_state()\n    await bot.answer_message(f"Your text is {user_text}")\n\n\nbot = Bot(\n    collectors=[\n        collector,\n    ],\n    bot_accounts=[\n        BotAccountWithSecret(\n            # Не забудьте заменить эти учётные данные на настоящие,\n            # когда создадите бота в панели администратора.\n            id=UUID("123e4567-e89b-12d3-a456-426655440000"),\n            host="cts.example.com",\n            secret_key="e29b417773f2feab9dac143ee3da20c5",\n        ),\n    ],\n    middlewares=[\n        FSMMiddleware([fsm], state_repo_key="redis_repo"),\n    ],\n)\n```\n\n\n### Передача данных между состояниями\n```python #fsm_storage\n@fsm.on(FsmStates.INPUT_FIRST_NAME)\nasync def input_first_name(message: IncomingMessage, bot: Bot) -> None:\n    first_name = message.body\n    await message.state.fsm.change_state(\n        FsmStates.INPUT_LAST_NAME,\n        first_name=first_name,\n    )\n    await bot.answer_message("Input your last name:")\n\n\n@fsm.on(FsmStates.INPUT_LAST_NAME)\nasync def input_last_name(message: IncomingMessage, bot: Bot) -> None:\n    first_name = message.state.fsm_storage.first_name\n    last_name = message.body\n    await message.state.fsm.drop_state()\n    await bot.answer_message(f"Hello {first_name} {last_name}!")\n```\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
