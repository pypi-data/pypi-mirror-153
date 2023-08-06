# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynautobot', 'pynautobot.core', 'pynautobot.models']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.20.0,<3.0.0']

extras_require = \
{':extra == "docs"': ['Sphinx>=3.5.1,<4.0.0']}

setup_kwargs = {
    'name': 'pynautobot',
    'version': '1.1.2',
    'description': 'Nautobot API client library',
    'long_description': '![pynautobot](docs/nautobot_logo.svg "Nautobot logo")\n\n# Pynautobot [![build main](https://travis-ci.com/nautobot/pynautobot.svg?branch=main)](https://travis-ci.com/nautobot/pynautobot)\nPython API client library for [Nautobot](https://github.com/nautobot/nautobot).\n\n> Pynautobot was initially developed as a fork of [pynetbox](https://github.com/digitalocean/pynetbox/).\n  Pynetbox was originally developed by Zach Moody at DigitalOcean and the NetBox Community.\n\n\nThe complete documentation for pynautobot can be found at [Read the Docs](https://pynautobot.readthedocs.io/en/stable/).\n\nQuestions? Comments? Join us in the **#nautobot** Slack channel on [Network to Code](https://networktocode.slack.com)!\n\n## Installation\n\nYou can install via [pip](#using-pip) or [poetry](#using-poetry)\n\n### Using pip\n\n```shell\n$ pip install pynautobot\n...\n```\n\n### Using poetry\n\n```shell\n$ git clone https://github.com/nautobot/pynautobot.git\n...\n$ pip install poetry\n...\n$ poetry shell\nVirtual environment already activated: /home/user/pynautobot/.venv\n$ poetry install\n...\n```\n\n\n## Quick Start\n\nA short introduction is provided here; the full documention for pynautobot is at [Read the Docs](http://pynautobot.readthedocs.io/).\n\nTo begin, import pynautobot and instantiate an `Api` object, passing the `url` and `token`.\n\n```python\nimport pynautobot\nnautobot = pynautobot.api(\n    url="http://localhost:8000",\n    token="d6f4e314a5b5fefd164995169f28ae32d987704f",\n)\n```\n\nThe Api object provides access to the Apps in Nautobot.\nThe Apps provide access to the Models and the field data stored in Nautobot.\nPynautobot uses the `Endpoint` class to represent Models.\nFor example, here is how to access **Devices** stored in Nautobot:\n\n```python\ndevices = nautobot.dcim.devices\ndevices\n<pynautobot.core.endpoint.Endpoint object at 0x7fe801e62fa0>\n```\n\n## Queries\n\nPynautobot provides several ways to retrieve objects from Nautobot.\nOnly the `get()` method is show here.\nTo continue from the example above, the `Endpoint` object returned will be used to `get`\nthe device named _hq-access-01_.\n\n```python\nswitch = devices.get(nam="hq-access-01")\n```\n\nThe object returned from the `get()` method is an implementation of the `Record` class.\nThis object provides access to the field data from Nautobot.\n\n```python\nswitch.id\n\'6929b68d-8f87-4470-8377-e7fdc933a2bb\'\nswitch.name\n\'hq-access-01\'\nswitch.site\nhq\n```\n\n### Threading\n\nPynautobot supports multithreaded calls for `.filter()` and `.all()` queries. It is **highly recommended** you have `MAX_PAGE_SIZE` in your Nautobot install set to anything *except* `0` or `None`. The default value of `1000` is usually a good value to use. To enable threading, add `threading=True` parameter when instantiating the `Api` object:\n\n```python\nnautobot = pynautobot.api(\n    url="http://localhost:8000",\n    token="d6f4e314a5b5fefd164995169f28ae32d987704f",\n    threading=True,\n)\n```\n\n### Versioning\n\nUsed for Nautobot Rest API versioning. Versioning can be controlled globally by setting `api_version` on initialization of the `API` class and/or for a specific request e.g (`list()`, `get()`, `create()` etc.) by setting an optional `api_version` parameter.\n\n__Global versioning__\n```python\nimport pynautobot\nnautobot = pynautobot.api(\n    url="http://localhost:8000",\n    token="d6f4e314a5b5fefd164995169f28ae32d987704f",\n    api_version="1.3"\n)\n```\n\n__Request specific versioning__\n```python\nimport pynautobot\nnautobot = pynautobot.api(\n  url="http://localhost:8000", token="d6f4e314a5b5fefd164995169f28ae32d987704f",\n)\ntags = nautobot.extras.tags\ntags.create(name="Tag", slug="tag", api_version="1.2",)\ntags.list(api_version="1.3",)\n```\n\n## Related projects\n\nPlease see [our wiki](https://github.com/nautobot/nautobot/wiki/Related-Projects)\nfor a list of relevant community projects.\n',
    'author': 'Network to Code, LLC',
    'author_email': 'opensource@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://nautobot.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
