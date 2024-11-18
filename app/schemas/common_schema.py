from enum import Enum


class IOrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"


class IInviteStatusEnum(str, Enum):
    pending = "pending"
    accepted = "accepted"
    declined = "declined"
