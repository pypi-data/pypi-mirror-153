# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_cloud_logging']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.71', 'google-cloud-logging>=3,<4']

setup_kwargs = {
    'name': 'fastapi-cloud-logging',
    'version': '1.0.0',
    'description': 'Cloud Logging For FastAPI',
    'long_description': '# fastapi-cloud-logging\n\n[![Test](https://github.com/quoth/fastapi-cloud-logging/actions/workflows/test.yaml/badge.svg)](https://github.com/quoth/fastapi-cloud-logging/actions/workflows/test.yaml)\n\n## Project description\n\nfastapi-cloud-logging improves cloud logging with fastapi. It enables to send request data on cloud logging.\n\n## Dependencies\n\n* fastapi\n* cloud logging\n* Python >= 3.7\n  * Require [contextvars](https://docs.python.org/3/library/contextvars.html)\n\n## Installation\n\n```sh\npip install fastapi-cloud-logging\n```\n\n## Usage\n\nAdd a middleware and set a handler to send a request info with each logging.\n\n```python\nfrom fastapi import FastAPI\nfrom google.cloud.logging import Client\nfrom google.cloud.logging_v2.handlers import setup_logging\n\nfrom fastapi_cloud_logging import FastAPILoggingHandler, RequestLoggingMiddleware\n\napp = FastAPI()\n\n# Add middleware\napp.add_middleware(RequestLoggingMiddleware)\n\n# Use manual handler\nhandler = FastAPILoggingHandler(Client())\nsetup_logging(handler)\n```\n\n## Optional\n\n### Structured Message\n\nCloud logging supports log entries with structured and unstructured data.\nWhen a log record has a structured data, it write a log entry with structured data. And when a log record contains a string message, it write a log entry as an unstructured textPayload attribute.\n\nWhen this structured option set True on FastAPILoggingHandler, it always write a log entry with a message attribute on a structured jsonPayload object.\n\n```python\n# default structured value is False\nhandler = FastAPILoggingHandler(Client(), structured=True)\n```\n\n## Changelog\n\n[`CHANGELOG.md`](CHANGELOG.md)\n\n## Appendix\n\n### With multithreading\n\nThis middleware depends mainly contextvars. So, when you use multithreading, it cannot handle a request info. On this case, you write a code for manual context management. For example, use `copy_context` on a thread.\n\nFor more information, please read [a great article about contextvars][1].\n\n[1]: https://kobybass.medium.com/python-contextvars-and-multithreading-faa33dbe953d\n',
    'author': 'quoth',
    'author_email': '4wordextinguisher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/quoth/fastapi-cloud-logging',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
