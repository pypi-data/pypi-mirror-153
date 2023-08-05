import os

from uuid import uuid4

from django_stomp.builder import build_publisher
from django_stomp.services.producer import auto_open_close_connection

from jsm_transactional_ruler.events import Event

USER_TRANSACTIONS_TOPIC = os.getenv("USER_TRANSACTIONS_TOPIC", "/topic/VirtualTopic.user-transactions")


def publish_event(event_trigger: Event, queue: str = USER_TRANSACTIONS_TOPIC, **publisher_parameters) -> None:
    """
    :param event_trigger: Body sended to queue
    :param queue: Define queue/topic to publish message
    :param publisher_parameters: Use to send additional parameters to method publisher.send from django-stomp.
        send(self, body: dict, queue: str, headers=None, persistent=True, attempt=10)
    """

    publish = build_publisher(f"transactional-ruler-{uuid4()}")

    with auto_open_close_connection(publish):
        publish.send(body=event_trigger.to_dict(), queue=queue, **publisher_parameters)
