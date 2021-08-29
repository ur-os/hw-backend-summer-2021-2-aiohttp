from dataclasses import dataclass


# Базовые структуры, для выполнения задания их достаточно,
# поэтому постарайтесь не менять их пожалуйста из-за возможных проблем с тестами

@dataclass
class UpdateMessage:
    id: int
    from_id: int
    text: str


@dataclass
class UpdateObject:
    UpdateMessage: UpdateMessage


@dataclass
class Update:
    type: str
    object: UpdateObject


@dataclass
class Message:
    user_id: int
    text: str


