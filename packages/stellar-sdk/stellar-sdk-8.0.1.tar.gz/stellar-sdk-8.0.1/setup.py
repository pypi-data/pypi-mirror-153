# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stellar_sdk',
 'stellar_sdk.call_builder',
 'stellar_sdk.call_builder.base',
 'stellar_sdk.call_builder.call_builder_async',
 'stellar_sdk.call_builder.call_builder_sync',
 'stellar_sdk.client',
 'stellar_sdk.operation',
 'stellar_sdk.sep',
 'stellar_sdk.xdr',
 'stellar_sdk.xdr2']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.4.0,<2.0.0',
 'aiohttp-sse-client>=0.2.1,<0.3.0',
 'aiohttp>=3.8.1,<4.0.0',
 'mnemonic>=0.20,<0.21',
 'requests>=2.26.0,<3.0.0',
 'stellar-base-sseclient>=0.0.21,<0.0.22',
 'toml>=0.10.2,<0.11.0',
 'typeguard>=2.13.0,<3.0.0',
 'urllib3>=1.26.7,<2.0.0']

setup_kwargs = {
    'name': 'stellar-sdk',
    'version': '8.0.1',
    'description': 'The Python Stellar SDK library provides APIs to build transactions and connect to Horizon.',
    'long_description': 'Stellar Python SDK\n==================\n\n.. image:: https://img.shields.io/github/workflow/status/StellarCN/py-stellar-base/GitHub%20Action/master?maxAge=1800\n    :alt: GitHub Action\n    :target: https://github.com/StellarCN/py-stellar-base/actions\n\n.. image:: https://img.shields.io/readthedocs/stellar-sdk.svg?maxAge=1800\n    :alt: Read the Docs\n    :target: https://stellar-sdk.readthedocs.io/en/latest/\n\n.. image:: https://static.pepy.tech/personalized-badge/stellar-sdk?period=total&units=abbreviation&left_color=grey&right_color=brightgreen&left_text=Downloads\n    :alt: PyPI - Downloads\n    :target: https://pypi.python.org/pypi/stellar-sdk\n\n.. image:: https://img.shields.io/codeclimate/maintainability/StellarCN/py-stellar-base?maxAge=1800\n    :alt: Code Climate maintainability\n    :target: https://codeclimate.com/github/StellarCN/py-stellar-base/maintainability\n\n.. image:: https://img.shields.io/codecov/c/github/StellarCN/py-stellar-base/v2?maxAge=1800\n    :alt: Codecov\n    :target: https://codecov.io/gh/StellarCN/py-stellar-base\n\n.. image:: https://img.shields.io/pypi/v/stellar-sdk.svg?maxAge=1800\n    :alt: PyPI\n    :target: https://pypi.python.org/pypi/stellar-sdk\n\n.. image:: https://img.shields.io/badge/python-%3E%3D3.6-blue\n    :alt: Python - Version\n    :target: https://pypi.python.org/pypi/stellar-sdk\n\n.. image:: https://img.shields.io/badge/implementation-cpython%20%7C%20pypy-blue\n    :alt: PyPI - Implementation\n    :target: https://pypi.python.org/pypi/stellar-sdk\n\n.. image:: https://img.shields.io/badge/Stellar%20Protocol-19-blue\n    :alt: Stellar Protocol\n    :target: https://developers.stellar.org/docs/glossary/scp/\n\npy-stellar-base is a Python library for communicating with\na `Stellar Horizon server`_. It is used for building Stellar apps on Python. It supports **Python 3.6+** as\nwell as PyPy 3.6+.\n\nIt provides:\n\n- a networking layer API for Horizon endpoints.\n- facilities for building and signing transactions, for communicating with a Stellar Horizon instance, and for submitting transactions or querying network history.\n\nDocumentation\n-------------\npy-stellar-base\'s documentation can be found at https://stellar-sdk.readthedocs.io.\n\nInstalling\n----------\n\n.. code-block:: text\n\n    pip install -U stellar-sdk\n\nWe follow `Semantic Versioning 2.0.0 <https://semver.org/>`_, and I strongly\nrecommend that you specify its major version number in the dependency\nfile to avoid the unknown effects of breaking changes.\n\nA Simple Example\n----------------\nYou can find more examples `here <https://github.com/StellarCN/py-stellar-base/tree/v8/examples>`__.\n\nBuilding transaction with synchronous server\n\n.. code-block:: python\n\n    # Alice pay 10.25 XLM to Bob\n    from stellar_sdk import Asset, Server, Keypair, TransactionBuilder, Network\n\n    alice_keypair = Keypair.from_secret("SBFZCHU5645DOKRWYBXVOXY2ELGJKFRX6VGGPRYUWHQ7PMXXJNDZFMKD")\n    bob_address = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"\n\n    server = Server("https://horizon-testnet.stellar.org")\n    alice_account = server.load_account(alice_keypair.public_key)\n    base_fee = 100\n    transaction = (\n        TransactionBuilder(\n            source_account=alice_account,\n            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,\n            base_fee=base_fee,\n        )\n        .add_text_memo("Hello, Stellar!")\n        .append_payment_op(bob_address, Asset.native(), "10.25")\n        .set_timeout(30)\n        .build()\n    )\n    transaction.sign(alice_keypair)\n    response = server.submit_transaction(transaction)\n    print(response)\n\n\n* Building transaction with asynchronous server\n\n.. code-block:: python\n\n    # Alice pay 10.25 XLM to Bob\n    import asyncio\n\n    from stellar_sdk import Asset, ServerAsync, Keypair, TransactionBuilder, Network\n    from stellar_sdk.client.aiohttp_client import AiohttpClient\n\n    alice_keypair = Keypair.from_secret("SBFZCHU5645DOKRWYBXVOXY2ELGJKFRX6VGGPRYUWHQ7PMXXJNDZFMKD")\n    bob_address = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"\n\n\n    async def payment():\n        async with ServerAsync(\n            horizon_url="https://horizon-testnet.stellar.org", client=AiohttpClient()\n        ) as server:\n            alice_account = await server.load_account(alice_keypair.public_key)\n            base_fee = 100\n            transaction = (\n                TransactionBuilder(\n                    source_account=alice_account,\n                    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,\n                    base_fee=base_fee,\n                )\n                .add_text_memo("Hello, Stellar!")\n                .append_payment_op(bob_address, Asset.native(), "10.25")\n                .set_timeout(30)\n                .build()\n            )\n            transaction.sign(alice_keypair)\n            response = await server.submit_transaction(transaction)\n            print(response)\n\n\n    if __name__ == "__main__":\n        asyncio.run(payment())\n\nstellar-model\n-------------\nstellar-model allows you to parse the JSON returned by Stellar Horizon\ninto the Python models, click `here <https://github.com/StellarCN/stellar-model>`__ for more information.\n\nLinks\n-----\n* Document: https://stellar-sdk.readthedocs.io\n* Code: https://github.com/StellarCN/py-stellar-base\n* Examples: https://github.com/StellarCN/py-stellar-base/tree/v8/examples\n* Issue tracker: https://github.com/StellarCN/py-stellar-base/issues\n* License: `Apache License 2.0 <https://github.com/StellarCN/py-stellar-base/blob/master/LICENSE>`_\n* Releases: https://pypi.org/project/stellar-sdk/\n\nThank you to all the people who have already contributed to py-stellar-base!\n\n.. _Stellar Horizon server: https://github.com/stellar/go/tree/master/services/horizon',
    'author': 'overcat',
    'author_email': '4catcode@gmail.com',
    'maintainer': 'overcat',
    'maintainer_email': '4catcode@gmail.com',
    'url': 'https://github.com/StellarCN/py-stellar-base',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
