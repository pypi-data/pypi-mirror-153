# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_firebase']

package_data = \
{'': ['*']}

install_requires = \
['google-auth>=2.6.0,<2.7.0', 'httpx<1.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

setup_kwargs = {
    'name': 'async-firebase',
    'version': '2.0.1',
    'description': 'Async Firebase Client - a Python asyncio client to interact with Firebase Cloud Messaging in an easy way.',
    'long_description': '# async-firebase is a lightweight asynchronous client to interact with Firebase Cloud Messaging for sending push notification to Android and iOS devices\n\n[![PyPI download total](https://img.shields.io/pypi/dt/async-firebase.svg)](https://pypi.python.org/pypi/async-firebase/)\n[![PyPI download month](https://img.shields.io/pypi/dm/async-firebase.svg)](https://pypi.python.org/pypi/async-firebase/)\n[![PyPI version fury.io](https://badge.fury.io/py/async-firebase.svg)](https://pypi.python.org/pypi/async-firebase/)\n[![PyPI license](https://img.shields.io/pypi/l/async-firebase.svg)](https://pypi.python.org/pypi/async-firebase/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/async-firebase.svg)](https://pypi.python.org/pypi/async-firebase/)\n[![GitHub Workflow Status for CI](https://img.shields.io/github/workflow/status/healthjoy/async-firebase/CI?label=CI&logo=github)](https://github.com/healthjoy/async-firebase/actions?query=workflow%3ACI)\n[![Codacy coverage](https://img.shields.io/codacy/coverage/b6a59cdf5ca64eab9104928d4f9bbb97?logo=codacy)](https://app.codacy.com/gh/healthjoy/async-firebase/dashboard)\n\n\n  * Free software: MIT license\n  * Requires: Python 3.6+\n\n## Features\n\n  * Extremely lightweight and does not rely on ``firebase-admin`` which is hefty\n  * Send push notifications to Android and iOS devices\n  * Send Multicast push notification to Android and iOS devices\n  * Set TTL (time to live) for notifications\n  * Set priority for notifications\n  * Set collapse-key for notifications\n  * Dry-run mode for testing purpose\n\n## Installation\n```shell script\n$ pip install async-firebase\n```\n\n## Getting started\nTo send push notification to Android:\n```python3\nimport asyncio\n\nfrom async_firebase import AsyncFirebaseClient\n\n\nasync def main():\n    client = AsyncFirebaseClient()\n    client.creds_from_service_account_file("secret-store/mobile-app-79225efac4bb.json")\n\n    # or using dictionary object\n    # client.creds_from_service_account_info({...}})\n\n    device_token = "..."\n\n    android_config = client.build_android_config(\n        priority="high",\n        ttl=2419200,\n        collapse_key="push",\n        data={"discount": "15%", "key_1": "value_1", "timestamp": "2021-02-24T12:00:15"},\n        title="Store Changes",\n        body="Recent store changes",\n    )\n    response = await client.push(device_token=device_token, android=android_config)\n\n    print(response.sucess, response.message_id)\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\nTo send push notification to iOS:\n\n```python3\nimport asyncio\n\nfrom async_firebase import AsyncFirebaseClient\n\n\nasync def main():\n    client = AsyncFirebaseClient()\n    client.creds_from_service_account_file("secret-store/mobile-app-79225efac4bb.json")\n\n    # or using dictionary object\n    # client.creds_from_service_account_info({...}})\n\n    device_token = "..."\n\n    apns_config = client.build_apns_config(\n        priority="normal",\n        ttl=2419200,\n        apns_topic="store-updated",\n        collapse_key="push",\n        title="Store Changes",\n        alert="Recent store changes",\n        badge=1,\n        category="test-category",\n        custom_data={"discount": "15%", "key_1": "value_1", "timestamp": "2021-02-24T12:00:15"}\n    )\n    response = await client.push(device_token=device_token, apns=apns_config)\n\n    print(response.success)\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\nThis prints:\n\n```shell script\n{"name": "projects/mobile-app/messages/0:2367799010922733%7606eb557606ebff"}\n```\n\nTo manual construct message:\n```python3\nimport asyncio\nfrom datetime import datetime\n\nfrom async_firebase.messages import APNSConfig, APNSPayload, ApsAlert, Aps\nfrom async_firebase import AsyncFirebaseClient\n\n\nasync def main():\n    apns_config = APNSConfig(**{\n        "headers": {\n            "apns-expiration": str(int(datetime.utcnow().timestamp()) + 7200),\n            "apns-priority": "10",\n            "apns-topic": "test-topic",\n            "apns-collapse-id": "something",\n        },\n        "payload": APNSPayload(**{\n            "aps": Aps(**{\n                "alert": ApsAlert(title="some-title", body="alert-message"),\n                "badge": 0,\n                "sound": "default",\n                "content_available": True,\n                "category": "some-category",\n                "mutable_content": False,\n                "custom_data": {\n                    "link": "https://link-to-somewhere.com",\n                    "ticket_id": "YXZ-655512",\n                },\n            })\n        })\n    })\n\n    device_token = "..."\n\n    client = AsyncFirebaseClient()\n    client.creds_from_service_account_info({...})\n    response = await client.push(device_token=device_token, apns=apns_config)\n    print(response.success)\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\n## License\n\n``async-firebase`` is offered under the MIT license.\n\n## Source code\n\nThe latest developer version is available in a GitHub repository:\n[https://github.com/healthjoy/async-firebase](https://github.com/healthjoy/async-firebase)\n',
    'author': 'Aleksandr Omyshev',
    'author_email': 'oomyshev@healthjoy.com',
    'maintainer': 'Healthjoy Developers',
    'maintainer_email': 'developers@healthjoy.com',
    'url': 'https://github.com/healthjoy/async-firebase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<3.11',
}


setup(**setup_kwargs)
