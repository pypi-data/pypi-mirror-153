# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsm_transactional_ruler']

package_data = \
{'': ['*']}

install_requires = \
['Django', 'django-stomp>=4.2.0']

setup_kwargs = {
    'name': 'jsm-transactional-ruler',
    'version': '2.3.1',
    'description': 'Lib to post user events on transactional topics',
    'long_description': '# Transactional Ruler\n\nLib to post user events on transactional topics\n\n## Running tests and lint\n\n`docker-compose up integration-tests`\n`docker-compose up lint`\n\n## Installation\n\n`pip install jsm-transactional-ruler`\n\n## Example Usage\n\n```python\nfrom jsm_transactional_ruler.enums import EventType\nfrom jsm_transactional_ruler.events import Event\nfrom jsm_transactional_ruler.publisher import publish_event\n\nevent = Event(\n    user_id="fake_id", event_type=EventType.T_EVENT_REGISTERED_USER, data={"email": "teste@juntossomosmais.com.br"}\n)\npublish_event(event_trigger=event)\n```\n\nThe attribute `event_type` accepts only events registered in the `EventType` enum.\n\nThe `publish_event` method accepts the optional `queue` and `publisher_parameters` parameters to send to django-stomp:\n\n\n```python\nevent = Event(\n    user_id="fake_id", event_type=EventType.T_EVENT_REGISTERED_USER, data={"email": "teste@juntossomosmais.com.br"}\n)\npublish_event(event_trigger=event, queue="/topic/VirtualTopic.user-update-transactions", persistent=False)\n```\n\n## Versioning\nThis lib follows the [pypi version format](https://www.python.org/dev/peps/pep-0440/) with the convention of using \n_major_._minor_._patch_ version.\n\n### When to bump a patch version?\nBump the patch version if you are doing a quick fix, nothing that changes the library functionality.\n\n### When to bump the minor version?\nBump the minor version if you are adding new functionality without breaking backwards compatibility. For example, \nadding support to new events.\n\n### When to bump the major version?\nBump the major version if you are breaking backwards compatibility by adding new functionality or refactoring.\n\n## Contributing\n\nThis project uses a [trunk based development](https://trunkbaseddevelopment.com/) flow, so that we have only one long-lived branch (`master`).\n\nFor any development, simply create a branch from it and follow the flow described [below](#how-to-upload-lib-to-pypi).\n\n## How to upload lib to PyPI\n\nIt is necessary to update the lib version using the command below:\n\n```shell\n$ poetry version major|minor|patch\n```\n\nAfter generating the version:\n* Create a new branch with the files updated by Poetry\n* Open PR based on the `master` branch\n* Merge PR into the master\n* Generate a new release based on the version. [Document to generate release](https://docs.github.com/en/enterprise/2.13/user/articles/creating-releases)\n* After generating the new release "Github Actions" will upload the lib to PyPI using Poetry.\n* Good job!',
    'author': 'Juntos Somos Mais',
    'author_email': 'labs@juntossomosmais.com.br',
    'maintainer': 'Juntos Somos Mais',
    'maintainer_email': 'labs@juntossomosmais.com.br',
    'url': 'https://juntossomosmais.com.br',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
