# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryptronics']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cryptronics',
    'version': '1.0.4',
    'description': 'Easy to use crypto API for python.',
    'long_description': '# Что это?\nCryptronics - это удобная и простая Python обёртка для криптовалютных API сервисов:\n- octopusapisoftware.com (usdt TRC20)\n- cryptocurrencyapi.net (btc, ltc, doge, dash, bch)\n- etherapi.net (eth)\n- bnbapi.net (bnb)\n\n# Как этим пользоваться?\nВыше был приведен список сервисыв, а так же список поддерживаемых ими монет в скобках.\nВам необходимо зарегистрировать аккаунты в зависимости от необходимых вам монет и сгенерировать API ключи в личном кабинете каждого из сервисов.\n\n## Импорт и настройка\nДля начала работы необходимо импортировать класс Crypto и инициализировать его, передав в качестве параметров Ваши ключи. Обратите внимание, что передавать все ключи не обязательно, можете указывать только для необходимых Вам сервисов.\n``` python\nfrom Cryptronics.base_crypto import Crypto\n\ncrypto = Crypto(\n    _octopus_api_key=\'<Ваш API ключ>\',\n    _crypto_api_key=\'<Ваш API ключ>\',\n    _eth_api_key=\'<Ваш API ключ>\',\n    _bnb_api_key=\'<Ваш API ключ>\',\n)\n```\n## Доступные методы\n### create_wallet(token, tag)\nВ качестве параметров принимает:\n- token - тикер токена, под который нужно создать кошелек (usdt, btc, etc...)\n- tag - метка, идентификатор. Нужна для идентификации операции в апи сервисе\n\nНиже приведен пример создания кошелька для пользователя, где в качестве тэга используется строка с вставленным в неё ID пользователя\n``` python\nresponse = crypto.create_wallet("usdt", f"user-wallet-{user_id}")\n```\nВ response вернется словарь (dict) с адресом только что созданного кошелька и иной информацией в зависимости от задействованного API сервиса\n\n### send(token, to_address, amount, tag)\n`Токены будут отправлены с Вашего ОСНОВНОГО кошелька. Подробнее о принципах работы системы можете почитать в документации к octopusapisoftware или cryptocurrency`\nВ качестве параметров принимает:\n- token - тикер токена, под который нужно создать кошелек (usdt, btc, etc...)\n- to_address - адрес для отправки токенов (с основного кошелька)\n- amount\n- tag - метка, идентификатор. Нужна для идентификации кошелька в апи сервисе\n\nНиже приведен пример вывода средств пользователю вашей системы. В качестве аргументов передан токен usdt, адрес пользователя стандарта `TRC20`, сумма и тэг \n``` python\nresponse = crypto.send(\n    token="usdt",\n    to_address="<USDT-TRC20-ADDRESS>",\n    amount=200,\n    tag=f"user-withdraw-{user_id}-{operation_id}"\n)\n```\nВ response вернется словарь (dict) с ID вашей транзакции в блокчейн сети и иной информацией в зависимости от задействованного API сервиса.\n\n# TODO:\n- Возможность получить баланс ГЛАВНОГО кошелька, указав токен или сервис \n- Добавить возможность отслеживать количество подтверждений транзакции в блокчейн сети\n- Возможность отслеживать ожидаемое пополнение фиксированной, заранее известной суммы',
    'author': 'vsaverin',
    'author_email': 'vasiliy.saverin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
