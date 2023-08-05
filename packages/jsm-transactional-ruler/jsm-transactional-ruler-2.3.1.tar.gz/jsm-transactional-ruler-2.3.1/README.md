# Transactional Ruler

Lib to post user events on transactional topics

## Running tests and lint

`docker-compose up integration-tests`
`docker-compose up lint`

## Installation

`pip install jsm-transactional-ruler`

## Example Usage

```python
from jsm_transactional_ruler.enums import EventType
from jsm_transactional_ruler.events import Event
from jsm_transactional_ruler.publisher import publish_event

event = Event(
    user_id="fake_id", event_type=EventType.T_EVENT_REGISTERED_USER, data={"email": "teste@juntossomosmais.com.br"}
)
publish_event(event_trigger=event)
```

The attribute `event_type` accepts only events registered in the `EventType` enum.

The `publish_event` method accepts the optional `queue` and `publisher_parameters` parameters to send to django-stomp:


```python
event = Event(
    user_id="fake_id", event_type=EventType.T_EVENT_REGISTERED_USER, data={"email": "teste@juntossomosmais.com.br"}
)
publish_event(event_trigger=event, queue="/topic/VirtualTopic.user-update-transactions", persistent=False)
```

## Versioning
This lib follows the [pypi version format](https://www.python.org/dev/peps/pep-0440/) with the convention of using 
_major_._minor_._patch_ version.

### When to bump a patch version?
Bump the patch version if you are doing a quick fix, nothing that changes the library functionality.

### When to bump the minor version?
Bump the minor version if you are adding new functionality without breaking backwards compatibility. For example, 
adding support to new events.

### When to bump the major version?
Bump the major version if you are breaking backwards compatibility by adding new functionality or refactoring.

## Contributing

This project uses a [trunk based development](https://trunkbaseddevelopment.com/) flow, so that we have only one long-lived branch (`master`).

For any development, simply create a branch from it and follow the flow described [below](#how-to-upload-lib-to-pypi).

## How to upload lib to PyPI

It is necessary to update the lib version using the command below:

```shell
$ poetry version major|minor|patch
```

After generating the version:
* Create a new branch with the files updated by Poetry
* Open PR based on the `master` branch
* Merge PR into the master
* Generate a new release based on the version. [Document to generate release](https://docs.github.com/en/enterprise/2.13/user/articles/creating-releases)
* After generating the new release "Github Actions" will upload the lib to PyPI using Poetry.
* Good job!