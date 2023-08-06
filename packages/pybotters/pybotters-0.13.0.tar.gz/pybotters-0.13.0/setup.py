# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybotters', 'pybotters.models', 'pybotters.models.deprecated']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'rich>=10.1.0,<11.0.0',
 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'pybotters',
    'version': '0.13.0',
    'description': 'An advanced api client for python botters.',
    'long_description': "[![pytest](https://github.com/MtkN1/pybotters/actions/workflows/pytest.yml/badge.svg)](https://github.com/MtkN1/pybotters/actions/workflows/pytest.yml)\n\n# [Preview] pybotters\n\nAn advanced api client for python botters.\n\n## 📌 Description\n\n`pybotters`は[仮想通貨botter](https://note.com/hht/n/n61e6ecefd059)向けのPythonライブラリです。\n\n複数取引所に対応した非同期I/OのAPIクライアントであり、bot開発により素晴らしいDXを提供します。\n\n## 👩\u200d💻👨\u200d💻 In development\n\n`pybotters` は現在 ** **Previewバージョン** ** です。\n一部機能は開発中です。\n\n開発状況については [こちら(Issues)](https://github.com/MtkN1/pybotters/issues) を参照してください。\n\n## 🚀 Features\n\n- ✨ HTTP / WebSocket Client\n    - 複数取引所のプライベートAPIを自動認証\n    - [`aiohttp`](https://docs.aiohttp.org/)ライブラリを基盤とした非同期通信\n    - WebSocketの自動再接続、自動ハートビート\n- ✨ DataStore\n    - WebSocket用の自動データ保管クラス\n    - 参照渡しによる高速なデータ参照\n    - 取引所別データモデルの実装\n- ✨ Developer Experience\n    - `asyncio`ライブラリを利用した非同期プログラミング\n    - 型ヒントのサポート\n\n## 🏦 Exchanges\n\n| Name | API auth | DataStore | API docs |\n| --- | --- | --- | --- |\n| Bybit | ✅ | ✅ | [Official](https://bybit-exchange.github.io/docs/inverse) |\n| Binance | ✅ | ✅(USDⓈ-M) | [Official](https://binance-docs.github.io/apidocs/futures/en/) |\n| OKX | ✅ | ✅ | [Official](https://www.okx.com/docs-v5/en/) |\n| Phemex | ✅ | ✅ | [Official](https://github.com/phemex/phemex-api-docs) |\n| Bitget | ✅ | ✅ | [Official](https://bitgetlimited.github.io/apidoc/en/mix/) |\n| MEXC | ✅ | WIP | [Official](https://mxcdevelop.github.io/APIDoc/) / [v3](https://mxcdevelop.github.io/apidocs/spot_v3_en/) |\n| FTX | ✅ | ✅ | [Official](https://docs.ftx.com/) |\n| BitMEX | ✅ | ✅ | [Official](https://www.bitmex.com/app/apiOverview) |\n| bitFlyer | ✅ | ✅ | [Official](https://lightning.bitflyer.com/docs) |\n| GMO Coin | ✅ | ✅ | [Official](https://api.coin.z.com/docs/) |\n| Liquid | ✅ | WIP | [Official](https://document.liquid.com/) |\n| bitbank | ✅ | ✅ | [Official](https://docs.bitbank.cc/) |\n| Coincheck | ✅ | ✅ | [Official](https://coincheck.com/documents/exchange/api) |\n\n## 🐍 Requires\n\nPython 3.7+\n\n## 🛠 Installation\n\n```sh\npip install pybotters\n```\n\n## 🔰 Usage\n\n### Single exchange\n\n```python\nimport asyncio\nimport pybotters\n\napis = {\n    'bybit': ['BYBIT_API_KEY', 'BYBIT_API_SECRET'],\n}\n\nasync def main():\n    async with pybotters.Client(apis=apis, base_url='https://api.bybit.com') as client:\n        # REST API\n        resp = await client.get('/v2/private/position/list', params={'symbol': 'BTCUSD'})\n        data = await resp.json()\n        print(data)\n\n        # WebSocket API (with defautl print handler)\n        ws = await client.ws_connect(\n            url='wss://stream.bybit.com/realtime',\n            send_json={'op': 'subscribe', 'args': ['trade.BTCUSD', 'order', 'position']},\n        )\n        await ws # Ctrl+C to break\n\ntry:\n    asyncio.run(main())\nexcept KeyboardInterrupt:\n    pass\n```\n\n### Multiple exchanges\n\n```python\napis = {\n    'bybit': ['BYBIT_API_KEY', 'BYBIT_API_SECRET'],\n    'binance': ['BINANCE_API_KEY', 'BINANCE_API_SECRET'],\n}\n\nasync def main():\n    async with pybotters.Client(apis=apis) as client:\n        await client.post('https://api.bybit.com/v2/private/order/create', data={'symbol': 'BTCUSD', ...: ...})\n        ...\n        await client.post('https://dapi.binance.com/dapi/v1/order', data={'symbol': 'BTCUSD_PERP', ...: ...})\n        ...\n```\n\n## 📖 Wiki\n\n詳しい利用方法は👉[Wikiページへ](https://github.com/MtkN1/pybotters/wiki)\n\n現在こちらにに移行中です👉[Read the Docs](https://pybotters.readthedocs.io/ja/latest/)\n\n## 🗽 License\n\nMIT\n\n## 💖 Author\n\nTwitter:\nhttps://twitter.com/MtkN1XBt\n\nDiscord:\nhttps://discord.com/invite/CxuWSX9U69",
    'author': 'MtkN1',
    'author_email': '51289448+MtkN1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MtkN1/pybotters',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
