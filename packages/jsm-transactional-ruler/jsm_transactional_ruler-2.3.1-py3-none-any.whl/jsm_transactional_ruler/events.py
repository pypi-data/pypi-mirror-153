from typing import Dict
from typing import List
from typing import Optional

from .enums import EventType


class Event:
    __slots__ = ["user_id", "_event_type", "profile_list", "data"]

    def __init__(
        self,
        user_id: str,
        event_type: EventType,
        profile_list: Optional[str] = None,
        data: Optional[List[Dict[str, str]]] = None,
    ) -> None:
        self.user_id = user_id
        self.event_type = event_type
        self.profile_list = profile_list
        self.data = data

    @property
    def event_type(self):
        return self._event_type

    @event_type.setter
    def event_type(self, event_type):
        if not isinstance(event_type, EventType):
            raise AttributeError("event_type is not instance from EventType")
        self._event_type = event_type

    def to_dict(self) -> Dict:
        data = {
            "user_id": self.user_id,
            "event_type": self.event_type.value,
        }

        if self.data:
            data["data"] = self.data

        if self.profile_list:
            data["profile_list"] = self.profile_list

        return data
