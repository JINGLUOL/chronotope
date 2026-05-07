from dataclasses import dataclass


@dataclass
class ChatWidgetMessage:
    text: str
    avatar: str = None
    is_self: bool = False
    pass
